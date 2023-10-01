from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class CrudTestCases(APITestCase):
    def setUp(self):
        self.url = reverse('invoice')
        self.post_data = {"invoice_customer_name": "Vinay Chandra Joshi", "item_details": [
                {"description": "Apples", "quantity": 5, "unit_price": "2.50", "price": "12.50"},
                {"description": "Bread", "quantity": 3, "unit_price": "2.00", "price": "8.00"},
                {"description": "Milk", "quantity": 1, "unit_price": "3.50", "price": "3.50"},
                {"description": "Pasta", "quantity": 3, "unit_price": "0.00", "price": "3.00"},
                {"description": "Potato", "quantity": 1, "unit_price": "150", "price": "17.00"}
            ]
        }
        self.update_data = {"invoice_customer_name": "Vinay C. Joshi", "item_details": [
            {"description": "Apples", "quantity": 5, "unit_price": "5.50"},
            {"description": "Sugar", "quantity": 2, "unit_price": "75"},
            {"description": "Potato", "quantity": 0, "unit_price": "150", "price": "17.00"}
                ]
            }

    def test_create_invoice(self):
        response = self.client.post(self.url, self.post_data, format='json')
        output_data = response.json()
        print('Invout data sent for creation: ', self.post_data, '\n')
        print('Output data after creation: ', output_data, '\n')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # checking if all the objects are created
        self.assertEqual(len(self.post_data['item_details']), len(output_data['data']['item_details']))
        # checking name of the customer in the invoice being the same being same
        self.assertEqual(self.post_data['invoice_customer_name'], output_data['data']['invoice_customer_name'])

    def test_update_invoice(self):
        response = self.client.post(self.url, self.post_data, format='json')
        output_data = response.json()['data']
        url_updation = reverse('invoice_pk', args=[output_data['id']])
        response_updation = self.client.put(url_updation, self.update_data, format='json')
        updated_data = response_updation.json()['data']
        print('Output data after Fresh Creation: ', output_data, '\n')
        print('Data sending for updating the created fresh output data: ', self.update_data, '\n')
        print('Final Data after sending updation data: ', updated_data)
        self.assertEqual(response_updation.status_code, status.HTTP_200_OK)
        # checking name of the customer in the invoice being the same being same
        self.assertEqual(self.update_data['invoice_customer_name'], updated_data['invoice_customer_name'])

    def test_delete_invoice(self):
        response = self.client.post(self.url, self.post_data, format='json')
        output_data = response.json()['data']
        url_updation = reverse('invoice_pk', args=[output_data['id']])
        response_delete = self.client.delete(url_updation, self.update_data, format='json')
        response_updation = self.client.get(url_updation, self.update_data, format='json')
        # checking if the deleted item when requested responds a bad request or not
        self.assertEqual(response_updation.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invoice(self):
        response = self.client.post(self.url, self.post_data, format='json')
        output_data = response.json()['data']
        url_updation = reverse('invoice_pk', args=[output_data['id']])
        response_updation = self.client.get(url_updation, self.update_data, format='json')
        # checking if response is 200 ok or not
        self.assertEqual(response_updation.status_code, status.HTTP_200_OK)