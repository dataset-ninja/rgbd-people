Dataset **RGB-D People Dataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM0NDJfUkdCLUQgUGVvcGxlIERhdGFzZXQvcmdiZC1wZW9wbGUtZGF0YXNldC1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJwRVZCNERFcDZ5aUpYRXNiUWZIVWVzSHpOMDFHU2JIcllReFB1eTA1UWtVPSJ9)

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