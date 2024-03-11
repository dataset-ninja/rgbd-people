**RGB-D People Dataset** is a dataset for object detection and monocular depth estimation tasks. It is used in the surveillance and robotics industries. 

The dataset consists of 6798 images with 4700 labeled objects belonging to 1 single class (*person*).

Images in the RGB-D People Dataset dataset have bounding box annotations. There are 2098 (31% of the total) unlabeled images (i.e. without annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Alternatively, the dataset could be split into 3 camera positions: ***center camera*** (2266 images), ***left camera*** (2266 images), and ***right camera*** (2266 images), or into 3 visibility in the depth image: ***fully visible*** (2418 images), ***partially visible*** (2282 images), and ***hidden*** (0 objects). Additionally, every image contains information about ***timestamp*** and ***track***. Moreover, images are grouped by ***seq***. The dataset was released in 2023 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">University of Freiburg, Germany</span>.

<img src="https://github.com/dataset-ninja/rgbd-people/raw/main/visualizations/poster.png">
