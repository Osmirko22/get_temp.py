#!/usr/bin/env python

import decimal

# Where temperature is stored
# currently it is a motherboard temperature
SENSOR_TPL = '/sys/class/thermal/thermal_zone{num}/temp'

def get_temp(sensor_num=0, *, _template=SENSOR_TPL):
    """Read temperature and return as decimal.

    Note:
        This call is blocking, but is ought to return fast
    """
    # convert to int
    sensor_num = int(sensor_num)
    
    fname = _template.format(num=sensor_num)
    with open(fname, 'r') as file:
        val = file.readline().strip()

    # convert value to int, then to decimal
    val = int(val)
    # the value we got is temperature * 1000,
    # thus divide by 1000 to get actual value
    dec = decimal.Decimal(f'{val}.000') / 1000
    return dec



class Sensor:
    _TEMPLATE = '/sys/class/thermal/thermal_zone{num}/temp'
    _PREC = 3
    
    def __init__(self, sensor_num=0, *, _tpl=None):
        sensor_num = int(sensor_num)    # enforce convertability

        # get template through arg or use class-level default
        tpl = self._TEMPLATE if _tpl is None else _tpl
        # or (same as)
        # tpl = _tpl or self._TEMPLATE

        self.sensor = tpl.format(num=sensor_num)

    @classmethod
    def convert_temperature(cls, value):
        # convert value to int, then to decimal
        value = int(value)
        # the value we got is temperature * (10 ** PREC),
        # thus divide by (10 ** PREC) to get actual value
        PREC = cls._PREC
        val = f'{value}.' + '0' * PREC
        dec = decimal.Decimal(val) / (10 ** PREC)
        return dec
    
    def get_temperature_raw(self):
        with open(self.sensor, 'r') as file:
            val = file.readline().strip()

        return val

    def get_temperature(self):
        # print('calc performed')       # uncomment to check it's cached
        val = self.get_temperature_raw()
        return self.convert_temperature(val)

    @property
    def temp(self):
        if not hasattr(self, '_temp'):
            self._temp = self.get_temperature()
        return self._temp          
    

class MicrophoneNoiseSensor(Sensor):
    _TEMPLATE = '/path/to/microphone_noise{num}'  # Template of the path to the noise level sensor from the microphone

    def __init__(self, sensor_num=0, *, _tpl=None):
        """
        Class for working with a microphone noise level sensor, inherited from Sensor.

        :param sensor_num: Number of the microphone noise sensor.
        :param _tpl: Custom path template to the microphone noise sensor.
        """
        super().__init__(sensor_num, _tpl=_tpl)

    def get_noise_level(self):
        """
        Gets the noise level value from the microphone.

        :return: The noise level from the microphone.
        """
        return self.get_temperature()  # Replace this function with the actual method to obtain the noise floor


class CameraColorSensor(Sensor):
    _TEMPLATE = '/path/to/camera_color{num}'  # Webcam colour sensor path template

    def __init__(self, sensor_num=0, *, _tpl=None):
        """
        Class for working with a webcam colour sensor, inherited from Sensor.

        :param sensor_num: Webcam colour sensor number.
        :param _tpl: Custom path template to the webcam's colour sensor.
        """
        super().__init__(sensor_num, _tpl=_tpl)

    def get_camera_color(self):
        """
        Gets colour values from a webcam.

        :return: Colour values from a webcam.
        """
        return self.get_temperature()  # Replace this function with the actual method to get the colour


if __name__ == '__main__':
    tmp = Sensor()
    val = tmp.get_temperature_raw()
    res = tmp.convert_temperature(val)
    # or
    res = tmp.temp
    # or
    res = Sensor(0).temp

    microphone_sensor = MicrophoneNoiseSensor()
    noise_level = microphone_sensor.get_noise_level()
    print(f"Microphone Noise Level: {noise_level}")

    camera_color_sensor = CameraColorSensor()
    camera_color = camera_color_sensor.get_camera_color()
    print(f"Camera Color: {camera_color}")
