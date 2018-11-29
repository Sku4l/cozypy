from cozypy.exception import CozytouchException
from cozypy.objects import CozytouchDevice, CozytouchPlace

class SetupHandler:

    def __init__(self, response):
        self.places = []

        data = response.json()

        self.__build_places(data["setup"]["rootPlace"])
        self.__build_devices(data["setup"]["devices"])


    def __build_places(self, place):
        for subPlace in place["subPlaces"]:
            self.__build_places(subPlace)
        self.places.append(CozytouchPlace(place))

    def __build_devices(self, devices):
        for data in devices:
            place:CozytouchPlace = self.__find_place(data["placeOID"])
            if place is None:
                raise CozytouchException("Place %s not found" % data["placeOID"])
            device = CozytouchDevice(data=data)
            place.add_device(device)

    def __find_place(self, oid):
        for place in self.places:
            if place.oid == oid:
                return place
        return None
