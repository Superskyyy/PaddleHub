import os
import shutil
import unittest

import cv2
import requests
import paddlehub as hub


class TestHubModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        img_url = 'https://ai-studio-static-online.cdn.bcebos.com/68313e182f5e4ad9907e69dac9ece8fc50840d7ffbd24fa88396f009958f969a'
        if not os.path.exists('tests'):
            os.makedirs('tests')
        response = requests.get(img_url)
        assert response.status_code == 200, 'Network Error.'
        with open('tests/test.jpg', 'wb') as f:
            f.write(response.content)
        cls.module = hub.Module(name="ssd_vgg16_512_coco2017")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('tests')
        shutil.rmtree('inference')
        shutil.rmtree('detection_result')

    def test_object_detection1(self):
        results = self.module.object_detection(
            paths=['tests/test.jpg']
        )
        bbox = results[0]['data'][0]
        label = bbox['label']
        confidence = bbox['confidence']
        left = bbox['left']
        right = bbox['right']
        top = bbox['top']
        bottom = bbox['bottom']

        self.assertEqual(label, 'cat')
        self.assertTrue(confidence > 0.5)
        self.assertTrue(200 < left < 800)
        self.assertTrue(2500 < right < 3500)
        self.assertTrue(500 < top < 1500)
        self.assertTrue(3500 < bottom < 4500)

    def test_object_detection2(self):
        results = self.module.object_detection(
            images=[cv2.imread('tests/test.jpg')]
        )
        bbox = results[0]['data'][0]
        label = bbox['label']
        confidence = bbox['confidence']
        left = bbox['left']
        right = bbox['right']
        top = bbox['top']
        bottom = bbox['bottom']

        self.assertEqual(label, 'cat')
        self.assertTrue(confidence > 0.5)
        self.assertTrue(200 < left < 800)
        self.assertTrue(2500 < right < 3500)
        self.assertTrue(500 < top < 1500)
        self.assertTrue(3500 < bottom < 4500)

    def test_object_detection3(self):
        results = self.module.object_detection(
            images=[cv2.imread('tests/test.jpg')],
            visualization=False
        )
        bbox = results[0]['data'][0]
        label = bbox['label']
        confidence = bbox['confidence']
        left = bbox['left']
        right = bbox['right']
        top = bbox['top']
        bottom = bbox['bottom']

        self.assertEqual(label, 'cat')
        self.assertTrue(confidence > 0.5)
        self.assertTrue(200 < left < 800)
        self.assertTrue(2500 < right < 3500)
        self.assertTrue(500 < top < 1500)
        self.assertTrue(3500 < bottom < 4500)

    def test_object_detection4(self):
        self.assertRaises(
            AssertionError,
            self.module.object_detection,
            paths=['no.jpg']
        )

    def test_object_detection5(self):
        self.assertRaises(
            cv2.error,
            self.module.object_detection,
            images=['test.jpg']
        )

    def test_save_inference_model(self):
        self.module.save_inference_model('./inference/model')

        self.assertTrue(os.path.exists('./inference/model.pdmodel'))
        self.assertTrue(os.path.exists('./inference/model.pdiparams'))


if __name__ == "__main__":
    unittest.main()
