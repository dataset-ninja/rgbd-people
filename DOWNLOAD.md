Dataset **RGB-D People Dataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/k/Q/ty/6fmQ8USMgieDH64dAo2beYNwYZm2sgmec3X1lYNdHmwp4QcoFn1UYimlMn06O6gFtax6ZppRnuVRb2Szt71DI7GXnmK0TmW0qF8ubD23U4jZ5pqubXvf0Z3nZiTg.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='RGB-D People Dataset', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](http://www.informatik.uni-freiburg.de/~spinello/sw/rgbd_people_unihall.tar.gz).