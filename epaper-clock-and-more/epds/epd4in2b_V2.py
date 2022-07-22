# *****************************************************************************
# * | File        :	  epd4in2bc.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
import epds.epdconfig as epdconfig

# Display resolution
EPD_WIDTH       = 400
EPD_HEIGHT      = 300
# GDEW042T2 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
DATA_START_TRANSMISSION_2                   = 0x13
LUT_FOR_VCOM                                = 0x20 
LUT_WHITE_TO_WHITE                          = 0x21
LUT_BLACK_TO_WHITE                          = 0x22
LUT_WHITE_TO_BLACK                          = 0x23
LUT_BLACK_TO_BLACK                          = 0x24
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_SENSOR_SELECTION                = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
RESOLUTION_SETTING                          = 0x61
GSST_SETTING                                = 0x65
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
READ_VCOM_VALUE                             = 0x81
VCM_DC_SETTING                              = 0x82
PARTIAL_WINDOW                              = 0x90
PARTIAL_IN                                  = 0x91
PARTIAL_OUT                                 = 0x92
PROGRAM_MODE                                = 0xA0
ACTIVE_PROGRAMMING                          = 0xA1
READ_OTP                                    = 0xA2
POWER_SAVING                                = 0xE3


logger = logging.getLogger(__name__)

class EPD:

    lut_vcom0 =         bytearray(b'\x40\x17\x00\x00\x00\
                                    x02\x00\x17\x17\x00\
                                    x00\x02\x00\x0A\x01\
                                    x00\x00\x01\x00\x0E\
                                    x0E\x00\x00\x02\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00\x00\x00')
    lut_ww =            bytearray(b'\x40\x17\x00\x00\x00\
                                    x02\x90\x17\x17\x00\
                                    x00\x02\x40\x0A\x01\
                                    x00\x00\x01\xA0\x0E\
                                    x0E\x00\x00\x02\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    lut_bw =            bytearray(b'\x40\x17\x00\x00\x00\
                                    x02\x90\x17\x17\x00\
                                    x00\x02\x40\x0A\x01\
                                    x00\x00\x01\xA0\x0E\
                                    x0E\x00\x00\x02\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    lut_bb =            bytearray(b'\x80\x17\x00\x00\x00\
                                    x02\x90\x17\x17\x00\
                                    x00\x02\x80\x0A\x01\
                                    x00\x00\x01\x50\x0E\
                                    x0E\x00\x00\x02\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    lut_wb =            bytearray(b'\x80\x17\x00\x00\x00\
                                    x02\x90\x17\x17\x00\
                                    x00\x02\x80\x0A\x01\
                                    x00\x00\x01\x50\x0E\
                                    x0E\x00\x00\x02\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    #common
    lut_vcom0_quick =   bytearray(b'\x00\x0E\x00\x00\x00\
                                    x01\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00\x00\x00')
    #WW -> --
    lut_ww_quick =      bytearray(b'\xA0\x0E\x00\x00\x00\
                                    x01\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    #BW R
    lut_bw_quick =      bytearray(b'\xA0\x0E\x00\x00\x00\
                                    x01\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    #WB W
    lut_bb_quick =      bytearray(b'\x50\x0E\x00\x00\x00\
                                    x01\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')
    #BB b
    lut_wb_quick =      bytearray(b'\x50\x0E\x00\x00\x00\
                                    x01\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\
                                    x00\x00\x00\x00\x00\x00\x00')

    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.fast_count = 0
        self.max_fast_refresh = 10
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(5)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)
    def _send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte(data)
        epdconfig.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        logger.debug("e-Paper busy")
        self.send_command(0x71);
        while(epdconfig.digital_read(self.busy_pin) == 0): # 0: idle, 1: busy
            self.send_command(0x71);
            epdconfig.delay_ms(20)
        logger.debug("e-Paper busy release")
            
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
            
        self.reset()
        
        self.send_command(0x04); 
        self.ReadBusy();

        self.send_command(0x00);
        self.send_data(0x0f);
        
        return 0

    def get_frame_buffer(self, image):
        # logger.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logger.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if(imwidth == self.width and imheight == self.height):
            # logger.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            # logger.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def set_lut(self, quick=False):
        print(self.lut_vcom0)
        if quick:
            self.fast_count = self.fast_count+1
            
            self.send_command(LUT_FOR_VCOM)
            self._send_data(self.lut_vcom0_quick)    # vcom

            self.send_command(LUT_WHITE_TO_WHITE)
            self._send_data(self.lut_ww_quick) # ww --

            self.send_command(LUT_BLACK_TO_WHITE)
            self._send_data(self.lut_bw_quick) # bw r

            self.send_command(LUT_WHITE_TO_BLACK)
            self._send_data(self.lut_wb_quick) # wb w

            self.send_command(LUT_BLACK_TO_BLACK)
            self._send_data(self.lut_bb_quick) # bb b         
        else:
            self.fast_count = 1
            self.send_command(LUT_FOR_VCOM)
            self._send_data(self.lut_vcom0)    # vcom

            self.send_command(LUT_WHITE_TO_WHITE)
            self._send_data(self.lut_ww) # ww --

            self.send_command(LUT_BLACK_TO_WHITE)
            self._send_data(self.lut_bw) # bw r

            self.send_command(LUT_WHITE_TO_BLACK)
            self._send_data(self.lut_wb) # wb w

            self.send_command(LUT_BLACK_TO_BLACK)
            self._send_data(self.lut_bb) # bb b


    def display_frame(self, imageblack, imagered):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])
        
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])
        
        self.set_lut(quick=(self.fast_count < self.max_fast_refresh or self.fast_count == 0))

        self.send_command(DISPLAY_REFRESH) 
        epdconfig.delay_ms(20)
        self.ReadBusy()

        
    def Clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
            
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        
        self.send_command(0x12) 
        epdconfig.delay_ms(20)
        self.ReadBusy()

    def sleep(self):
        self.send_command(0X50);
        self.send_data(0xf7);		#border floating	

        self.send_command(0X02);  	#power off
        self.ReadBusy(); #waiting for the electronic paper IC to release the idle signal
        self.send_command(0X07);  	#deep sleep
        self.send_data(0xA5);
        
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
### END OF FILE ###

