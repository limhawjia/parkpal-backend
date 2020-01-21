from main.database.carpark import CarPark
from main.database import Database
import main.geocoding as gc


# Method to add/update the database with new carpark metadata. If the provided data model does not contain a
# longitude and latitude, it is populated use Google's geocoding services in this method. Existing carparks
# whose addresses have not changed will not be added/updated.
def update_carpark_metadata(carpark_data_models):
    gc_use_count = 0
    carpark_add_count = 0
    carpark_modified_count = 0
    session = Database.get_instance().get_session()

    for carpark in carpark_data_models:
        query = session.query(CarPark) \
            .filter(CarPark.source == carpark.source) \
            .filter(CarPark.third_party_id == carpark.third_party_id) \
            .first()

        if not query:
            carpark_with_coordinates, gc_used = populate_carpark_data_model_with_coordinates(carpark)

            if gc_used:
                gc_use_count = gc_use_count + 1

            if carpark_with_coordinates is not None:
                session.add(carpark_with_coordinates)
                session.commit()
                carpark_add_count = carpark_add_count + 1

            continue

        if query.address != carpark.address:
            carpark_with_coordinates, gc_used = populate_carpark_data_model_with_coordinates(carpark)

            if gc_used:
                gc_use_count = gc_use_count + 1

            if carpark_with_coordinates is not None:
                query.address = carpark_with_coordinates.address
                query.latitude = carpark_with_coordinates.latitude
                query.longitude = carpark_with_coordinates.longitude
                session.commit()
                carpark_modified_count = carpark_modified_count + 1

            continue

    session.close()
    print(f'{len(carpark_data_models)} carparks were pulled.')
    print(f'{carpark_add_count} new carparks were added.')
    print(f'{carpark_modified_count} carparks were modified.')
    print(f'Google\'s geocoding services used {gc_use_count} times.')


# Helper method to call Google's geocoding services
def populate_carpark_data_model_with_coordinates(carpark_data_model):
    if carpark_data_model.latitude is not None and carpark_data_model.longitude is not None:
        return carpark_data_model, False
    else:
        return gc.update_data_model_with_coordinates(carpark_data_model), True


# Method to update carpark availability. The carpark must exist within the database for this method call to
# succeed. If the carpark has not been already registered in the database, this method call is ignored. The data set
# parameter is a tuple consisting of the source, third party id and lots available.
def update_carpark_availability(data_sets):
    session = Database.get_instance().get_session()

    for data in data_sets:
        source = data[0]
        third_party_id = data[1]
        lots_available = data[2]

        query = session.query(CarPark) \
            .filter(CarPark.source == source) \
            .filter(CarPark.third_party_id == third_party_id) \
            .first()

        if not query:
            continue

        query.lots_available = lots_available
        session.commit()

    session.close()
