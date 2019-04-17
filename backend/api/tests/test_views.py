import json
import os

import PyPDF2
import pytest
from api.views import UploadResumeView, HealthCheckView
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import filesizeformat
from django.urls import reverse


class TestUploadResumeView:

    def make_pdf_file(self, file_name, size):
        pdf = PyPDF2.PdfFileWriter()
        pdf.name = file_name
        current_size = 306
        while current_size < size:
            pdf.addBlankPage(width=100, height=100)
            current_size += 116
        with open(pdf.name, 'wb') as output:
            pdf.write(output)
        return pdf.name

    def test_request_without_file(self, rf):
        request = rf.post(reverse('upload_resume'))
        response = UploadResumeView.as_view()(request)

        assert response.status_code == 400

        content = json.loads(response.content)
        assert content['error'] == 'there is no file'

    def test_request_with_no_valid_file(self, rf):
        # MAX_TEST_FILE_SIZE = 5 * 1024 * 1024
        # NUMBER_OF_FILE_PAIRS = 1
        #
        # uploaded_files_name = []
        # for i in range(0, NUMBER_OF_FILE_PAIRS):
        #     uploaded_files_name.append(self.make_pdf_file(f"{i}.pdf", random.randint(0,
        #                                                                             UploadResumeView.validator.min_size)))  # min pdf file size is 306 bytes
        #     uploaded_files_name.append(self.make_pdf_file(f"{i}.pdf", random.randint(UploadResumeView.validator.max_size,
        #                                                                             MAX_TEST_FILE_SIZE)))
        #
        # uploaded_files_size = []
        # for i in range(0, NUMBER_OF_FILE_PAIRS):
        #     uploaded_files_size[i] = os.stat(uploaded_files_name[i]).st_size
        upload_file_name = self.make_pdf_file('1.pdf', UploadResumeView.validator.min_size - 1)
        upload_file_size = os.stat(upload_file_name).st_size

        with open(upload_file_name) as upload_file:
            request = rf.post(reverse('upload_resume'), {'file': upload_file})
        response = UploadResumeView.as_view()(request)
        content = json.loads(response.content)

        assert response.status_code == 400
        assert content.get('error') == f"The current file {filesizeformat(upload_file_size)},\
which is too small. The minumum file size is {filesizeformat(UploadResumeView.validator.min_size)}."

    @pytest.mark.django_db
    def test_request_with_valid_file(self, rf):
        upload_file_name = self.make_pdf_file('1.pdf', UploadResumeView.validator.max_size - (1 * 1024 * 1024))

        with open(upload_file_name) as upload_file:
            request = rf.post(reverse('upload_resume'), {'file': upload_file})
        response = UploadResumeView.as_view()(request)

        assert response.status_code == 201
        assert os.path.exists(FileSystemStorage('CVs/').location)

        response = UploadResumeView.as_view()(request)
        content = json.loads(response.content)

        assert response.status_code == 400
        assert content.get('error') == 'file with same name already exists'

    @pytest.mark.django_db
    def test_delete_request(self, rf):
        request = rf.delete(reverse('upload_resume'))
        response = UploadResumeView.as_view()(request)

        assert response.status_code == 200


class TestHealthCheckView:
    def test_get_request(self, rf):
        request = rf.get(reverse('health_check'))
        response = HealthCheckView.as_view()(request)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('server') == 'pong' and content.get('database') == 'pong'

    def test_broken_db(self, rf):
        os.environ['DB_NAME'] = "DB"
        request = rf.get(reverse('health_check'))
        response = HealthCheckView.as_view()(request)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('server') == 'pong' and content.get('database') == 'error'
