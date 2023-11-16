import { Icon } from "leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

const defaultMarker = new Icon({
  iconUrl: markerIconPng,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

export { defaultMarker };
