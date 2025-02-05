import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

import { defaultMarker } from "./Icons";

const LeafletMap = (props) => {
  //Just centered on Atlanta by default
  const center = [33.6488, -84.2877];

  const [positions, setPositions] = useState([]);

  useEffect(() => {
    const fetchPositions = () => {
      fetch(`http://django:8000/data/pos/`)
        .then((response) => response.json())
        .then((data) => {
          setPositions(data.map((pos) => [pos.latitude, pos.longitude]));
        })
        .catch((error) => {
          console.error("Failed to fetch data from endpoint:", error);
        });
    };

    fetchPositions();
    const interval = setInterval(fetchPositions, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <MapContainer className="map" center={center} zoom={5}>
        <TileLayer
          attribution='&amp;copy <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {positions.map((position, index) => {
          return (
            <Marker key={index} position={position} icon={defaultMarker}>
              <Popup>
                A pretty CSS3 popup. <br /> Easily customizable.
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </>
  );
};

export default LeafletMap;
