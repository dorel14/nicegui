from typing import Callable, Optional

from fastapi import Request, Response

from ..dependencies import register_component
from ..element import Element
from ..events import UploadEventArguments, handle_event
from ..nicegui import app

register_component('upload', __file__, 'upload.vue')


class Upload(Element):

    def __init__(self, *,
                 multiple: bool = False,
                 on_upload: Optional[Callable] = None,
                 file_picker_label: str = '',
                 auto_upload: bool = False,
                 upload_button_icon: str = 'file_upload') -> None:
        """File Upload

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param on_upload: callback to execute when a file is uploaded (list of bytearrays)
        :param file_picker_label: label for the file picker element
        :param upload_button_icon: icon for the upload button
        """
        super().__init__('upload')
        self.classes('row items-center gap-2')
        self._props['multiple'] = multiple
        self._props['file_picker_label'] = file_picker_label
        self._props['auto_upload'] = auto_upload
        self._props['upload_button_icon'] = upload_button_icon
        self._props['url'] = f'/_nicegui/upload/{self.id}'

        @app.post(f'/_nicegui/upload/{self.id}')
        async def upload_route(request: Request) -> Response:
            for data in (await request.form()).values():
                args = UploadEventArguments(
                    sender=self,
                    client=self.client,
                    content=data.file,
                    name=data.filename,
                    type=data.content_type,
                )
                handle_event(on_upload, args)
            return {'upload': 'success'}

    def reset(self) -> None:
        self.run_method('reset')
