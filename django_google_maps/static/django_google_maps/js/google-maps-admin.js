
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/

function googleMapAdmin() {

    var autocompleteStart;
    var autocompleteEnd;
    var geocoder = new google.maps.Geocoder();
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay;
    var map;
    var markerStart;
    var markerEnd;
    var startPoint;
    var endPoint;

    var addressStartId = 'id_address_start';
    var addressEndId = 'id_address_end';
    var waypointsId = 'id_waypoints';
    var addressStartLatId = 'id_address_start_lat';
    var addressStartLngId = 'id_address_start_lng';
    var addressEndLatId = 'id_address_end_lat';
    var addressEndLngId = 'id_address_end_lng';

    var searchAddressStartId = 'id_search_address_start';
    var searchAddressEndId = 'id_search_address_end';
    var searchAddressStartLatId = 'id_search_address_start_lat';
    var searchAddressStartLngId = 'id_search_address_start_lng';
    var searchAddressEndLatId = 'id_search_address_end_lat';
    var searchAddressEndLngId = 'id_search_address_end_lng';

    var self = {
        initialize: function() {
            // set up initial map to be world view. also, add change
            // event so changing address will update the map
//            var existinglocation = self.getExistingLocation();
            directionsDisplay = new google.maps.DirectionsRenderer();

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    lat = position.coords.latitude;
                    lng = position.coords.longitude;
                    var latlng = new google.maps.LatLng(lat,lng);
                    self.initializeMap(latlng)
                })
            }else{
                var latlng = new google.maps.LatLng(0,0);
                self.initializeMap(latlng);
            }


        },

        initializeMap : function(latlng){
            var zoom = 10;
            var myOptions = {
              zoom: zoom,
              center: latlng,
              mapTypeId: self.getMapType()
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            autocompleteStart = new google.maps.places.Autocomplete(
                /** @type {!HTMLInputElement} */(document.getElementById(addressStartId)),
                {types: ['geocode']});

            autocompleteEnd = new google.maps.places.Autocomplete(
                /** @type {!HTMLInputElement} */(document.getElementById(addressEndId)),
                {types: ['geocode']});

            // this only triggers on enter, or if a suggested location is chosen
            // todo: if a user doesn't choose a suggestion and presses tab, the map doesn't update
            autocompleteStart.addListener("place_changed",
                                    func=function(){self.codeAddress(addressStartId, autocompleteStart)},false);
            autocompleteEnd.addListener("place_changed",
                                    func=function(){self.codeAddress(addressEndId, autocompleteEnd)},false);

            // don't make enter submit the form, let it just trigger the place_changed event
            // which triggers the map update & geocode
            $("#" + addressStartId).keydown(function (e) {
                if (e.keyCode == 13) {  // enter key
                    e.preventDefault();
                    return false;
                }
            });
            $("#" + addressEndId).keydown(function (e) {
                if (e.keyCode == 13) {  // enter key
                    e.preventDefault();
                    return false;
                }
            });
        },

        getMapType : function() {
            return google.maps.MapTypeId.HYBRID;
        },

        codeAddress: function(id, autocomplete) {
            var place = autocomplete.getPlace();
            if(place.geometry !== undefined) {
                self.updateWithCoordinates(id, place.geometry.location);
            }
            else {
                geocoder.geocode({'address': place.name}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        var latlng = results[0].geometry.location;
                        self.updateWithCoordinates(id, latlng);
                    } else {
                        alert("Geocode was not successful for the following reason: " + status);
                    }
                });
            }
        },

        updateWithCoordinates: function(id, latlng) {
            map.setCenter(latlng);
            map.setZoom(18);
            if(id===addressStartId){
                self.setMarkerStart(id, latlng);
            }else if(id===addressEndId){
                self.setMarkerEnd(id, latlng);
            }
            self.updateGeolocation(id, latlng);
        },

        setMarkerStart: function(id, latlng) {
            startPoint = latlng;
            if (markerStart) {
                markerStart.setPosition(latlng);
            } else {
               markerStart = new google.maps.Marker({
                    map: map,
                    position: latlng
                });

               markerStart.setDraggable(true);
               google.maps.event.addListener(markerStart, 'dragend', function(new_location) {
                   self.updateGeolocation(id, new_location.latLng);
               });
            }
        },

        setMarkerEnd: function(id, latlng) {
            endPoint = latlng;
            if (markerEnd) {
                markerEnd.setPosition(latlng);
            } else {
               markerEnd = new google.maps.Marker({
                    map: map,
                    position: latlng
                });

                markerEnd.setDraggable(true);
                google.maps.event.addListener(markerEnd, 'dragend', function(new_location) {
                    self.updateGeolocation(id, new_location.latLng);
                });
            }
        },

        updateGeolocation: function(id, latlng) {
            //document.getElementById(id).value = latlng.lat() + "," + latlng.lng();
            $("#" + id).trigger('change');
            if(markerStart && markerEnd) self.createRoute();
        },

        createRoute: function() {
            var bounds = new google.maps.LatLngBounds();
            bounds.extend(startPoint);
            bounds.extend(endPoint);
            map.fitBounds(bounds);
            var request = {
                origin: startPoint,
                destination: endPoint,
                travelMode: google.maps.TravelMode.DRIVING
            };
            directionsService.route(request, function (response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(response);
                    directionsDisplay.setMap(map);
                    document.getElementById(addressStartLatId).value = startPoint.lat();
                    document.getElementById(addressStartLngId).value = startPoint.lng();
                    document.getElementById(addressEndLatId).value = endPoint.lat();
                    document.getElementById(addressEndLngId).value = endPoint.lng();
                    document.getElementById(waypointsId).value = JSON.stringify(response);
                } else {
                    alert("Directions Request from " + start.toUrlValue(6) + " to " + end.toUrlValue(6) + " failed: " + status);
                }
            });
        },

        showRoute: function(route) {
            console.log(route);
        }
    };

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
});
