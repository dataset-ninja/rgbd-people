import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from PIL import Image
from supervisely.io.fs import get_file_name, mkdir, remove_dir
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/RGB-D Peoples/archive/mensa_seq0_1.1"
    images_path = "/home/alex/DATASETS/TODO/RGB-D Peoples/archive/mensa_seq0_1.1/rgb"
    depth_path = "/home/alex/DATASETS/TODO/RGB-D Peoples/archive/mensa_seq0_1.1/depth"
    tracks_path = "/home/alex/DATASETS/TODO/RGB-D Peoples/archive/mensa_seq0_1.1/track_annotations"
    batch_size = 30
    ds_name = "ds"
    images_ext = ".ppm"
    depth_ext = ".pgm"
    group_tag_name = "seq"
    new_image_ext = ".png"

    def create_ann(image_path):
        labels = []
        tags = []

        img = Image.open(image_path)
        img_height = img.height
        img_wight = img.width

        im_id_value = get_file_name(image_path)
        group_id = sly.Tag(tag_id, value=im_id_value)
        tags.append(group_id)

        camera_meta = idx_to_camera[get_file_name(image_path).split("_")[-1]]
        camera = sly.Tag(camera_meta)
        tags.append(camera)

        track_value = im_name_to_track.get(get_file_name(image_path))
        if track_value is not None:
            track = sly.Tag(tag_track, value=track_value)

            ann_data = im_name_to_data[get_file_name(image_path)]

            timestamp_value = float(ann_data[0])
            timestamp = sly.Tag(tag_timestamp, value=timestamp_value)

            visibility_meta = idx_to_visibility[int(ann_data[-1])]
            visibility = sly.Tag(visibility_meta)

            if image_path.split("/")[-2] == "rgb":
                left = int(ann_data[5])
                right = left + int(ann_data[7])
                top = int(ann_data[6])
                bottom = top + int(ann_data[8])
            else:
                left = int(ann_data[1])
                right = left + int(ann_data[3])
                top = int(ann_data[2])
                bottom = top + int(ann_data[4])

            rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
            label = sly.Label(rectangle, obj_class)
            labels.append(label)

            tags.extend([visibility, timestamp, track])

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("person", sly.Rectangle)
    tag_track = sly.TagMeta("track", sly.TagValueType.ANY_NUMBER)
    tag_timestamp = sly.TagMeta("timestamp", sly.TagValueType.ANY_NUMBER)
    tag_hidden = sly.TagMeta("hidden", sly.TagValueType.NONE)
    tag_fully = sly.TagMeta("fully visible", sly.TagValueType.NONE)
    tag_partially = sly.TagMeta("partially visible", sly.TagValueType.NONE)
    tag_left = sly.TagMeta("left camera", sly.TagValueType.NONE)
    tag_center = sly.TagMeta("center camera", sly.TagValueType.NONE)
    tag_right = sly.TagMeta("right camera", sly.TagValueType.NONE)

    idx_to_visibility = {0: tag_hidden, 1: tag_fully, 2: tag_partially}
    idx_to_camera = {"0": tag_left, "1": tag_center, "2": tag_right}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    tag_id = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[
            tag_track,
            tag_timestamp,
            tag_hidden,
            tag_left,
            tag_id,
            tag_fully,
            tag_partially,
            tag_center,
            tag_right,
        ],
    )

    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    im_name_to_track = {}
    im_name_to_data = {}
    for track_file in os.listdir(tracks_path):
        track_number = int(get_file_name(track_file).split("_")[1])
        curr_track_path = os.path.join(tracks_path, track_file)
        with open(curr_track_path) as f:
            content = f.read().split("\n")
            for idx, curr_data in enumerate(content):
                if idx == 0:
                    continue
                if len(curr_data) > 0:
                    curr_data = curr_data.split(" ")
                    im_name_to_track[curr_data[0]] = track_number
                    im_name_to_data[curr_data[0]] = curr_data[1:]

    images_names = os.listdir(images_path)
    depth_names = os.listdir(depth_path)

    for curr_names, curr_path in [(images_names, images_path), (depth_names, depth_path)]:
        progress = sly.Progress("Create dataset {}".format(ds_name), len(curr_names))

        for img_names_batch in sly.batched(curr_names, batch_size=batch_size):
            img_pathes_batch = [os.path.join(curr_path, im_name) for im_name in img_names_batch]

            # TODO =========================== must have, import images does not accept .ppm, .pgm ext ===
            temp_img_pathes_batch = []
            temp_folder = os.path.join(dataset_path, "temp")
            mkdir(temp_folder)
            for im_path in img_pathes_batch:
                temp_img = Image.open(im_path)
                new_img_path = os.path.join(temp_folder, get_file_name(im_path) + new_image_ext)
                temp_img_pathes_batch.append(new_img_path)
                temp_img.save(new_img_path)

            # TODO =======================================================================================

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, temp_img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            remove_dir(temp_folder)
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))

    return project
