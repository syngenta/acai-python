import unittest
from syngenta_digital_alc.s3.s3_key_pivoter import S3KeyPivoter


class TestS3KeyPivoter(unittest.TestCase):

    def setUp(self):
        self.test_key = (
            '/normalized/088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863/operation/00f80775-7a68-561b-8fcb-0685aa450f7b-spatial.geojson'
        )

    def test_parse_filename(self):
        result = S3KeyPivoter.parse_key(self.test_key)

        self.assertEqual(result.data_stage, 'normalized')
        self.assertEqual(result.account_id, '088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863')
        self.assertEqual(result.entity, 'operation')
        self.assertEqual(result.operation_id, '00f80775-7a68-561b-8fcb-0685aa450f7b')

    def test_build_spatial(self):
        actual = S3KeyPivoter.parse_key(self.test_key)
        self.assertEqual(
            'normalized/088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863/operation/00f80775-7a68-561b-8fcb-0685aa450f7b-spatial.geojson',
            actual.file_spatial()
        )

    def test_build_summary(self):
        actual = S3KeyPivoter.parse_key(self.test_key)
        self.assertEqual(
            'normalized/088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863/operation/00f80775-7a68-561b-8fcb-0685aa450f7b-summary.json',
            actual.file_summary()
        )

    def test_build_unbuffered_rectangle(self):
        actual = S3KeyPivoter.parse_key(self.test_key)
        self.assertEqual(
            'normalized/088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863/operation/00f80775-7a68-561b-8fcb-0685aa450f7b-rectangular-unbuffered.geojson',
            actual.file_rectangular_unbuffered()
        )

    def test_build_unbuffered_rectangle_downsampled(self):
        actual = S3KeyPivoter.parse_key(self.test_key)
        self.assertEqual(
            'normalized/088ae889-25a2-40fa-ab3d-1c3895e2134a_35eb0cbf-9fa6-49fc-ad4c-03179eac9863/operation/00f80775-7a68-561b-8fcb-0685aa450f7b-rectangular-unbuffered-downsampled.geojson',
            actual.file_rectangular_unbuffered_downsampled()
        )

    def test_build_summary_pivot(self):
        actual = S3KeyPivoter.parse_key(self.test_key)
        self.assertEqual(
            'normalized/account_id/operation/operation_id-rectangular-unbuffered-downsampled.geojson',
            actual.file_rectangular_unbuffered_downsampled(account_id='account_id', operation_id='operation_id')
        )
