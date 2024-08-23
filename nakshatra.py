from collections import namedtuple as struct
from datetime import date, datetime
import swisseph as swe
import pytz

Place = struct("Place", ["latitude", "longitude", "timezone"])

# Hard-coding Nagpur coordinates
nagpur = Place(21.14631, 79.08491, +5.30)

set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_LAHIRI)
reset_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

gregorian_to_jd = lambda date, time: swe.julday(date.year, date.month, date.day, time)

class Nakshatra:
    '''
    Class for calculating current Nakshatra and other information.
    
    It uses `swisseph` library to get the angle measurement from the
    current time w.r.t to a planet (`MOON`).
    '''

    LIST_OF_NAKSHATRAS = [
        "Ashvini",          "Bharani",          "Krutika",
        "Rohini",           "Mrugasirisha",     "Ardra",
        "Punarvasu",        "Pushya",           "Ashlesha",
        "Magha",            "Purvaphalguni",    "UttaraPhalguni",
        "Hasta",            "Chitra",           "Swati",
        "Vishakha",         "Anuradha",         "Jyeshtha",
        "Mula",             "Purvaashadha",     "Uttaraashadha",
        "Shravana",         "Dhanishta",        "Shatabhisha",
        "Purvabadrapada",   "Uttarabadrapada",  "Revati",
    ]

    LIST_OF_TITHIS = [
        "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", 
        "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", 
        "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi", 
        "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima", 
        "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", 
        "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", 
        "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi", 
        "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
    ]


    def pada(self, angle: float, precision: int = 1):
        """
        Calculate pada
        """
        nakshatra_angle = 4 * 3.333  # 4 times 3degrees 20 min
        rem = angle % nakshatra_angle
        return round(rem / (3.333), precision)

    def __calculate_angle(self, jd, planet, precision: int = 4):
        set_ayanamsa_mode()
        longi = swe.calc_ut(jd, planet, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        reset_ayanamsa_mode()
        return round(longi[0][0] % 360, precision)

    def get_tithi_and_angle(self, precision = 3):

        # Get the current time
        time, dt = self.get_time()
        today = datetime.strptime(str(dt), "%Y-%m-%d").date()

        # Convert to Julian Date
        jd = gregorian_to_jd(today, time)

        sun_long = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)[0][0]
        moon_long = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)[0][0]

        angle = (moon_long - sun_long + 360) % 360

        idx = int(angle // 12)

        return angle, Nakshatra.LIST_OF_TITHIS[idx]


    def get_time(self):
        """
        Get the current time as (no. of hours, time)
        """

        # Set the desired timezone (Kolkata)
        kolkata_timezone = pytz.timezone("Asia/Kolkata")
        # Get the current time in the Kolkata timezone
        current_time = datetime.now(kolkata_timezone)

        # Extract hours, minutes, and seconds from the datetime object
        hours = current_time.hour
        minutes = current_time.minute
        seconds = current_time.second

        # Convert minutes to hours
        minutes_in_hours = minutes / 60.0

        # Convert seconds to hours
        seconds_in_hours = seconds / 3600.0

        # Calculate the total time in hours as a floating-point number
        total_time_in_hours = hours + minutes_in_hours + seconds_in_hours

        return (total_time_in_hours, current_time.strftime("%Y-%m-%d"))

    def info(self, angle: float):
        """
        Returns the nakshatra information based on given angle 'name' and 'pada' as a dictionary
        """
        return {
            "name": self.LIST_OF_NAKSHATRAS[int(angle * 27 / 360)],
            "pada": self.pada(angle),
        }
    def get_angle_wrt_planet(self, planet) -> int:
        """
        Calculate the angle based on current time w.r.t to a given `planet`.
        """

        # Get the current time
        time, dt = self.get_time()
        today = datetime.strptime(str(dt), "%Y-%m-%d").date()

        # Convert to Julian Date
        jul_date = gregorian_to_jd(today, time)

        # Calculate the angle
        angle = self.__calculate_angle(jul_date, planet)

        # Return the angle, adjusting with error
        result = angle - 3.05
        if result < 0:
            return 360 + result
        
        return result
    
    def get_angle_wrt_moon(self) -> int:
        """
        Calculate the angle based on current time w.r.t to MOON
        """

        return self.get_angle_wrt_planet(swe.MOON)
