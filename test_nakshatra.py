from nakshatra import Nakshatra

nks = Nakshatra()

angle = nks.get_angle_wrt_moon()
print(f"Current Angle : {angle}")

print(f"Current Nakshatra : {nks.info(angle)}")