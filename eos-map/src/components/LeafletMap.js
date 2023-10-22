import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

import { defaultMarker } from './Icons';

const LeafletMap = (props) => {
	//Just centered on Atlanta by default
	const center = [33.7488, -84.3877];

	const [ position, setPosition ] = useState(center);

	useEffect(() => {
		const interval = setInterval(() => {
			console.log("This runs every second");
			//Must ping server for position here
		}, 1000);

		return () => clearInterval(interval);
	}, [position]);


	return (
		<MapContainer
			className='map'
			center={center}
			zoom={5}
		>
			<TileLayer
				attribution='&amp;copy <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
				url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			/>
			<Marker 
				position={position}
				icon={defaultMarker}
			>
				<Popup>
					A pretty CSS3 popup. <br /> Easily customizable.
				</Popup>
			</Marker>
		</MapContainer>
	)
};

export default LeafletMap;