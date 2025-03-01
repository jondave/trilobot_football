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

document.getElementById('opencv_goal').onclick = ev => {
    ev.preventDefault();
    sendCmd("opencv_goal");
};

document.getElementById('follow_goal').onclick = ev => {
    ev.preventDefault();
    sendCmd("follow_goal");
};

document.getElementById('custom_code').onclick = ev => {
    ev.preventDefault();
    sendCmd("custom_code");
};

// Speed slider Controls
const speedSlider = document.getElementById('speedSlider');
const speedLabel = document.getElementById('speedLabel');  // Assuming a label to show the speed value

speedSlider.addEventListener('input', () => {
    // Update the label element with the current speed value
    speedLabel.textContent = 'Speed (0-1): ' + speedSlider.value;
    // Send the speed value to the server
    sendCmd(`speed:${speedSlider.value}`);
});

// Color Range Sliders Ball
const hueMinInput = document.getElementById('hueMin');
const hueMaxInput = document.getElementById('hueMax');
const saturationMinInput = document.getElementById('saturationMin');
const saturationMaxInput = document.getElementById('saturationMax');
const intensityMinInput = document.getElementById('intensityMin');
const intensityMaxInput = document.getElementById('intensityMax');

// Display values for sliders Ball
const hueMinValue = document.getElementById('hueMinValue');
const hueMaxValue = document.getElementById('hueMaxValue');
const saturationMinValue = document.getElementById('saturationMinValue');
const saturationMaxValue = document.getElementById('saturationMaxValue');
const intensityMinValue = document.getElementById('intensityMinValue');
const intensityMaxValue = document.getElementById('intensityMaxValue');

// Update display values for sliders Ball
function updateValues() {
    hueMinValue.textContent = hueMinInput.value;
    hueMaxValue.textContent = hueMaxInput.value;
    saturationMinValue.textContent = saturationMinInput.value;
    saturationMaxValue.textContent = saturationMaxInput.value;
    intensityMinValue.textContent = intensityMinInput.value;
    intensityMaxValue.textContent = intensityMaxInput.value;
}

// Event listeners for sliders Ball
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
// Color Range Sliders Ball End

// Color Range Sliders Goal
const hueMinInputGoal = document.getElementById('hueMinGoal');
const hueMaxInputGoal = document.getElementById('hueMaxGoal');
const saturationMinInputGoal = document.getElementById('saturationMinGoal');
const saturationMaxInputGoal = document.getElementById('saturationMaxGoal');
const intensityMinInputGoal = document.getElementById('intensityMinGoal');
const intensityMaxInputGoal = document.getElementById('intensityMaxGoal');

// Display values for sliders Goal
const hueMinValueGoal = document.getElementById('hueMinValueGoal');
const hueMaxValueGoal = document.getElementById('hueMaxValueGoal');
const saturationMinValueGoal = document.getElementById('saturationMinValueGoal');
const saturationMaxValueGoal = document.getElementById('saturationMaxValueGoal');
const intensityMinValueGoal = document.getElementById('intensityMinValueGoal');
const intensityMaxValueGoal = document.getElementById('intensityMaxValueGoal');

// Update display values for sliders Goal
function updateValuesGoal() {
    hueMinValueGoal.textContent = hueMinInputGoal.value;
    hueMaxValueGoal.textContent = hueMaxInputGoal.value;
    saturationMinValueGoal.textContent = saturationMinInputGoal.value;
    saturationMaxValueGoal.textContent = saturationMaxInputGoal.value;
    intensityMinValueGoal.textContent = intensityMinInputGoal.value;
    intensityMaxValueGoal.textContent = intensityMaxInputGoal.value;
}

// Event listeners for sliders Goal
hueMinInputGoal.addEventListener('input', () => {
    const newHueMinGoal = parseFloat(hueMinInputGoal.value);
    const newHueMaxGoal = parseFloat(hueMaxInputGoal.value);
    
    if (!isNaN(newHueMinGoal) && newHueMinGoal <= newHueMaxGoal) {
        sendCmd(`hue_min_goal:${newHueMinGoal}`);
        updateValuesGoal();
    } else {
        hueMinInputGoal.value = newHueMaxGoal;  // Reset to max value if min exceeds max
    }
});

hueMaxInputGoal.addEventListener('input', () => {
    const newHueMaxGoal = parseFloat(hueMaxInputGoal.value);
    const newHueMinGoal = parseFloat(hueMinInputGoal.value);
    
    if (!isNaN(newHueMaxGoal) && newHueMaxGoal >= newHueMinGoal) {
        sendCmd(`hue_max_goal:${newHueMaxGoal}`);
        updateValuesGoal();
    } else {
        hueMaxInputGoal.value = newHueMinGoal;  // Reset to min value if max is less than min
    }
});

saturationMinInputGoal.addEventListener('input', () => {
    const newSaturationMinGoal = parseFloat(saturationMinInputGoal.value);
    const newSaturationMaxGoal = parseFloat(saturationMaxInputGoal.value);
    
    if (!isNaN(newSaturationMinGoal) && newSaturationMinGoal <= newSaturationMaxGoal) {
        sendCmd(`saturation_min_goal:${newSaturationMinGoal}`);
        updateValuesGoal();
    } else {
        saturationMinInputGoal.value = newSaturationMaxGoal;  // Reset to max value if min exceeds max
    }
});

saturationMaxInputGoal.addEventListener('input', () => {
    const newSaturationMaxGoal = parseFloat(saturationMaxInputGoal.value);
    const newSaturationMinGoal = parseFloat(saturationMinInputGoal.value);
    
    if (!isNaN(newSaturationMaxGoal) && newSaturationMaxGoal >= newSaturationMinGoal) {
        sendCmd(`saturation_max_goal:${newSaturationMaxGoal}`);
        updateValuesGoal();
    } else {
        saturationMaxInputGoal.value = newSaturationMinGoal;  // Reset to min value if max is less than min
    }
});

intensityMinInputGoal.addEventListener('input', () => {
    const newIntensityMinGoal = parseFloat(intensityMinInputGoal.value);
    const newIntensityMaxGoal = parseFloat(intensityMaxInputGoal.value);
    
    if (!isNaN(newIntensityMinGoal) && newIntensityMinGoal <= newIntensityMaxGoal) {
        sendCmd(`intensity_min_goal:${newIntensityMinGoal}`);
        updateValuesGoal();
    } else {
        intensityMinInputGoal.value = newIntensityMaxGoal;  // Reset to max value if min exceeds max
    }
});

intensityMaxInputGoal.addEventListener('input', () => {
    const newIntensityMaxGoal = parseFloat(intensityMaxInputGoal.value);
    const newIntensityMinGoal = parseFloat(intensityMinInputGoal.value);
    
    if (!isNaN(newIntensityMaxGoal) && newIntensityMaxGoal >= newIntensityMinGoal) {
        sendCmd(`intensity_max_goal:${newIntensityMaxGoal}`);
        updateValuesGoal();
    } else {
        intensityMaxInputGoal.value = newIntensityMinGoal;  // Reset to min value if max is less than min
    }
});

// Update values on page load
updateValues();
// Color Range Sliders Goal End

// AWSD Controls
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
    } else if (event.code === 'spaceAction') {
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

window.addEventListener("gamepadconnected", (event) => {
    controllerIndex = event.gamepad.index;
    console.log("Gamepad connected at index:", controllerIndex);
    requestAnimationFrame(updateController);
});

window.addEventListener("gamepaddisconnected", () => {
    console.log("Gamepad disconnected");
    controllerIndex = null;
});

let lastDirection = '';  // Initialize the variable

function updateController() {
    requestAnimationFrame(updateController); // 🔥 Guarantees updates every frame 🔥

    const gamepads = navigator.getGamepads();
    if (!gamepads || !gamepads[controllerIndex]) return;

    const gp = gamepads[controllerIndex];
    const leftX = parseFloat(gp.axes[0].toFixed(2));
    const leftY = parseFloat(gp.axes[1].toFixed(2));

    // console.log(`Joystick X: ${leftX}, Y: ${leftY}`);

    let direction = "stop";

    if (Math.abs(leftY) > Math.abs(leftX)) {
        if (leftY < -0.5) direction = "forward";
        else if (leftY > 0.5) direction = "backward";
    } else {
        if (leftX < -0.5) direction = "left";
        else if (leftX > 0.5) direction = "right";
    }

    if (direction !== lastDirection) {
        // console.log("New direction:", direction);
        lastDirection = direction;
        // sendCommand(direction);

        if (direction == "right") {
            sendCmd("right");
        } else if (direction == "left") {
            sendCmd("left");
        } else if (direction == "forward") {
            sendCmd("up");
        } else if (direction == "backward") {
            sendCmd("down");
        } else if (direction == "stop") {
            sendCmd("stop");
        }
    }
}