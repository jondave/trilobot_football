const socket = new WebSocket('ws://' + location.host + '/command');

function sendCmd(cmd) {
    console.log("Going " + cmd)
    socket.send(cmd);
}

// Debug
socket.addEventListener('message', ev => {
    console.log(ev.data)
});

// On Screen Controls
document.getElementById('left').onclick = ev => {
    ev.preventDefault();
    sendCmd("left")
};

document.getElementById('right').onclick = ev => {
    ev.preventDefault();
    sendCmd("right");
};

document.getElementById('up').onclick = ev => {
    ev.preventDefault();
    sendCmd("up");
};

document.getElementById('down').onclick = ev => {
    ev.preventDefault();
    sendCmd("down");
};

document.getElementById('stop').onclick = ev => {
    ev.preventDefault();
    sendCmd("stop");
};

document.getElementById('stop-mobile').onclick = ev => {
    ev.preventDefault();
    sendCmd("stop");
};

document.getElementById('opencv').onclick = ev => {
    ev.preventDefault();
    sendCmd("opencv");
};

document.getElementById('follow_ball').onclick = ev => {
    ev.preventDefault();
    sendCmd("follow_ball");
};

// Slider Controls
const speedSlider = document.getElementById('speedSlider');
const speedLabel = document.getElementById('speedLabel');  // Assuming a label to show the speed value

speedSlider.addEventListener('input', () => {
    // Update the label element with the current speed value
    speedLabel.textContent = 'Speed (0-1): ' + speedSlider.value;
    // Send the speed value to the server
    sendCmd(`speed:${speedSlider.value}`);
});

// Color Range Sliders
const hueMinInput = document.getElementById('hueMin');
const hueMaxInput = document.getElementById('hueMax');
const saturationMinInput = document.getElementById('saturationMin');
const saturationMaxInput = document.getElementById('saturationMax');
const intensityMinInput = document.getElementById('intensityMin');
const intensityMaxInput = document.getElementById('intensityMax');

// Display values for sliders
const hueMinValue = document.getElementById('hueMinValue');
const hueMaxValue = document.getElementById('hueMaxValue');
const saturationMinValue = document.getElementById('saturationMinValue');
const saturationMaxValue = document.getElementById('saturationMaxValue');
const intensityMinValue = document.getElementById('intensityMinValue');
const intensityMaxValue = document.getElementById('intensityMaxValue');

// Update display values for sliders
function updateValues() {
    hueMinValue.textContent = hueMinInput.value;
    hueMaxValue.textContent = hueMaxInput.value;
    saturationMinValue.textContent = saturationMinInput.value;
    saturationMaxValue.textContent = saturationMaxInput.value;
    intensityMinValue.textContent = intensityMinInput.value;
    intensityMaxValue.textContent = intensityMaxInput.value;
}

// Event listeners for sliders
hueMinInput.addEventListener('input', () => {
    const newHueMin = parseFloat(hueMinInput.value);
    const newHueMax = parseFloat(hueMaxInput.value);
    
    if (!isNaN(newHueMin) && newHueMin <= newHueMax) {
        sendCmd(`hue_min:${newHueMin}`);
        updateValues();
    } else {
        hueMinInput.value = newHueMax;  // Reset to max value if min exceeds max
    }
});

hueMaxInput.addEventListener('input', () => {
    const newHueMax = parseFloat(hueMaxInput.value);
    const newHueMin = parseFloat(hueMinInput.value);
    
    if (!isNaN(newHueMax) && newHueMax >= newHueMin) {
        sendCmd(`hue_max:${newHueMax}`);
        updateValues();
    } else {
        hueMaxInput.value = newHueMin;  // Reset to min value if max is less than min
    }
});

saturationMinInput.addEventListener('input', () => {
    const newSaturationMin = parseFloat(saturationMinInput.value);
    const newSaturationMax = parseFloat(saturationMaxInput.value);
    
    if (!isNaN(newSaturationMin) && newSaturationMin <= newSaturationMax) {
        sendCmd(`saturation_min:${newSaturationMin}`);
        updateValues();
    } else {
        saturationMinInput.value = newSaturationMax;  // Reset to max value if min exceeds max
    }
});

saturationMaxInput.addEventListener('input', () => {
    const newSaturationMax = parseFloat(saturationMaxInput.value);
    const newSaturationMin = parseFloat(saturationMinInput.value);
    
    if (!isNaN(newSaturationMax) && newSaturationMax >= newSaturationMin) {
        sendCmd(`saturation_max:${newSaturationMax}`);
        updateValues();
    } else {
        saturationMaxInput.value = newSaturationMin;  // Reset to min value if max is less than min
    }
});

intensityMinInput.addEventListener('input', () => {
    const newIntensityMin = parseFloat(intensityMinInput.value);
    const newIntensityMax = parseFloat(intensityMaxInput.value);
    
    if (!isNaN(newIntensityMin) && newIntensityMin <= newIntensityMax) {
        sendCmd(`intensity_min:${newIntensityMin}`);
        updateValues();
    } else {
        intensityMinInput.value = newIntensityMax;  // Reset to max value if min exceeds max
    }
});

intensityMaxInput.addEventListener('input', () => {
    const newIntensityMax = parseFloat(intensityMaxInput.value);
    const newIntensityMin = parseFloat(intensityMinInput.value);
    
    if (!isNaN(newIntensityMax) && newIntensityMax >= newIntensityMin) {
        sendCmd(`intensity_max:${newIntensityMax}`);
        updateValues();
    } else {
        intensityMaxInput.value = newIntensityMin;  // Reset to min value if max is less than min
    }
});

// Update values on page load
updateValues();

// WASD Controls
document.addEventListener('keydown', function (event) {
    if (event.code === 'KeyW') {
        sendCmd('up');
    } else if (event.code === 'KeyA') {
        sendCmd('left');
    } else if (event.code === 'KeyS') {
        sendCmd('down');
    } else if (event.code === 'KeyD') {
        sendCmd('right');
    } else if (event.code === 'KeyX') {
        sendCmd('stop');
    } else if (event.code === 'Enter') {
        return;
    }
});

// Function to fetch ultrasonic distance
function fetchUltrasonicData() {
    fetch('/get_ultrasonic_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // console.log("Distance: ", data.distance); // Replace with actual distance display logic
            // Example: Update distance on the page
            document.getElementById('ultrasonic_distance').innerText = `Distance: ${data.distance} cm`;
        })
        .catch(error => {
            console.error('Error fetching ultrasonic data:', error);
        });
}

// Start or stop fetching ultrasonic data
let isUltrasonicEnabled = false;
let fetchInterval;

document.getElementById('ultrasonic').onclick = ev => {
    ev.preventDefault();
    isUltrasonicEnabled = !isUltrasonicEnabled;

    if (isUltrasonicEnabled) {
        console.log("Starting ultrasonic data fetch...");
        document.getElementById('ultrasonic_distance').innerText = `Distance: Starting`;
        fetchInterval = setInterval(fetchUltrasonicData, 1000); // Fetch data every second
    } else {
        console.log("Stopping ultrasonic data fetch...");
        document.getElementById('ultrasonic_distance').innerText = `Distance: Stopped`;
        clearInterval(fetchInterval);
    }
};