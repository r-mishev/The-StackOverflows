import unittest
from unittest.mock import patch, MagicMock
import threading
import time
from embedded import controller as ctrl


# A fake serial class to simulate the SIM900 module.
class FakeSerial:
    def __init__(self, read_buffer=b""):
        self.write_log = []
        self.read_buffer = read_buffer

    def flushInput(self):
        self.read_buffer = b""

    def write(self, data):
        self.write_log.append(data)

    def read(self, size):
        # Return up to 'size' bytes from the read_buffer.
        result = self.read_buffer[:size]
        self.read_buffer = self.read_buffer[size:]
        return result

    def inWaiting(self):
        return len(self.read_buffer)

class TestController(unittest.TestCase):
    def setUp(self):
        # Clear the global served_numbers set before each test.
        ctrl.served_numbers.clear()

    @patch('time.sleep', return_value=None)  # Speed up tests by bypassing sleep.
    def test_init_sim900(self, mock_sleep):
        """
        Test that init_sim900 flushes input and writes the correct AT commands.
        """
        fake_serial = FakeSerial()
        # For simplicity, simulate that every read() returns b"OK\r\n".
        fake_serial.read = lambda size: b'OK\r\n'
        fake_serial.inWaiting = lambda: len(b'OK\r\n')

        ctrl.init_sim900(fake_serial)

        expected_writes = [b'AT\r', b'AT+CMGF=1\r', b'AT+CLIP=1\r']
        self.assertEqual(fake_serial.write_log, expected_writes)

    @patch('time.sleep', return_value=None)
    def test_send_sms(self, mock_sleep):
        """
        Test that send_sms writes the proper AT+CMGS command and SMS text (terminated with Ctrl+Z).
        """
        fake_serial = FakeSerial()
        # Simulate the SIM900 returning a prompt '>' when asked.
        fake_serial.read_buffer = b'>'
        fake_serial.inWaiting = lambda: len(b'>')

        phone_number = "+1234567890"
        test_message = "Test Message"
        ctrl.send_sms(fake_serial, phone_number, test_message)

        expected_command = f'AT+CMGS="{phone_number}"\r'.encode()
        expected_sms = test_message.encode() + b'\x1A'
        self.assertIn(expected_command, fake_serial.write_log)
        self.assertIn(expected_sms, fake_serial.write_log)

    @patch('requests.post')
    @patch('requests.get')
    def test_call_endpoint_with_location(self, mock_get, mock_post):
        """
        Test that call_endpoint retrieves location data and posts the expected payload.
        """
        # Create mock responses for the two GET calls.
        mock_ip_resp = MagicMock()
        mock_ip_resp.text = "1.2.3.4"
        mock_info_resp = MagicMock()
        mock_info_resp.json.return_value = {"loc": "12.34,56.78"}
        # First GET returns the IP, second returns the location info.
        mock_get.side_effect = [mock_ip_resp, mock_info_resp]

        ctrl.call_endpoint()

        # Verify calls were made with the expected URLs.
        mock_get.assert_any_call("https://api.ipify.org")
        mock_get.assert_any_call("https://ipinfo.io/1.2.3.4/json")
        # Verify the POST call with the correct payload.
        expected_payload = {"latitude": "12.34", "longitude": "56.78"}
        mock_post.assert_called_with("http://localhost:8080/detect", data=expected_payload)

    @patch('embedded.controller.send_sms')
    @patch('embedded.controller.call_endpoint')
    def test_process_unsolicited_new_number(self, mock_call_endpoint, mock_send_sms):
        """
        Test that process_unsolicited extracts a new phone number from a CLIP message,
        calls send_sms and call_endpoint, and adds the number to served_numbers.
        """
        fake_serial = FakeSerial()
        message = 'CLIP: "+1234567890",145,"",,"",0'
        ctrl.process_unsolicited(message, fake_serial)

        mock_send_sms.assert_called_once_with(fake_serial, "+1234567890", ctrl.SMS_MESSAGE)
        mock_call_endpoint.assert_called_once()
        self.assertIn("+1234567890", ctrl.served_numbers)

    @patch('embedded.controller.send_sms')
    @patch('embedded.controller.call_endpoint')
    def test_process_unsolicited_duplicate_number(self, mock_call_endpoint, mock_send_sms):
        """
        Test that if the same phone number is processed twice, send_sms and call_endpoint
        are only called once.
        """
        fake_serial = FakeSerial()
        phone_number = "+1234567890"
        message = f'CLIP: "{phone_number}",145,"",,"",0'
        # First unsolicited message.
        ctrl.process_unsolicited(message, fake_serial)
        # Duplicate unsolicited message.
        ctrl.process_unsolicited(message, fake_serial)

        mock_send_sms.assert_called_once_with(fake_serial, phone_number, ctrl.SMS_MESSAGE)
        mock_call_endpoint.assert_called_once()

    @patch('time.sleep', return_value=None)
    def test_monitor_serial(self, mock_sleep):
        fake_serial = FakeSerial()
        data = "RING\r\nCLIP: \"+1234567890\",145,\"\",,\"\",0\r\n"
        fake_serial.read_buffer = data.encode()

        # Replace process_unsolicited with a MagicMock.
        original_process_unsolicited = ctrl.process_unsolicited
        ctrl.process_unsolicited = MagicMock()

        monitor_thread = threading.Thread(target=ctrl.monitor_serial, args=(fake_serial,))
        monitor_thread.daemon = True
        monitor_thread.start()
        time.sleep(0.5)
        # Check that process_unsolicited was called at least twice.
        self.assertGreaterEqual(ctrl.process_unsolicited.call_count, 2)
        # Restore the original function.
        ctrl.process_unsolicited = original_process_unsolicited

if __name__ == '__main__':
    unittest.main()
