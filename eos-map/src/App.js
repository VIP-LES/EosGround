import './App.css';
import 'leaflet/dist/leaflet.css'
import LeafletMap from './components/LeafletMap';

function App() {
  return (
    <div className='app'>
      <h1 className='app-header'>
				Live Tracking Map
			</h1>
			<LeafletMap />
    </div>
  );
}

export default App;
