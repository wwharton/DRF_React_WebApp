import bear from './bear.svg';
import './AppBear.css';

function AppBear() {
  return (
    <div className="App">
      <header className="App-header-bear">
        <img src={bear} className="App-logo" alt="logo" />
      </header>
    </div>
  );
}

export default AppBear;
