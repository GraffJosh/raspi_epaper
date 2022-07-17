import os
from PIL import Image,ImageDraw,ImageFont
import epd2in7b_fast_lut as epaper_driver

class EPaper:
    EPD_WIDTH       = 400
    EPD_HEIGHT      = 300
    MONO_DISPLAY    = False

    def __init__(self) -> None:
    
        self._epd = epaper_driver.EPD(height=self.EPD_HEIGHT,width=self.EPD_WIDTH)
        self.blackbuffer = self._epd.get_frame_buffer()

        self._epd.draw_string_at(self, frame_buffer, x, y, text, font, colored):
        
        self._epd.display_frame(
            self._epd.get_frame_buffer(black_buf),
            self._epd.get_frame_buffer(red_buf)
        )