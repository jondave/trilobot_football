const socket = new WebSocket('ws://' + location.host + '/command');

function sendCmd(cmd) {
    console.log("Going " + cmd)
    socket.send(cmd);
}

// Debug
socket.addEventListener('message', ev => {
    console.log(message)
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

// Slider Controls
const speedSlider = document.getElementById('speedSlider');

speedSlider.addEventListener('input', () => {
    // Update the label element with the current speed value
    speedLabel.textContent = 'Speed (0-1): ' + speedSlider.value;
    // Send the speed value to the server
    sendCmd(`speed:${speedSlider.value}`);
});

// Box inputs
hueMinInput.addEventListener('input', () => {
    const newHueMin = parseFloat(hueMinInput.value);
    
    if (!isNaN(newHueMin)) {
        // Send the value to the server
        sendCmd(`hue_min:${newHueMin}`);
    }
});

hueMaxInput.addEventListener('input', () => {
    const newHueMax = parseFloat(hueMaxInput.value);
    
    if (!isNaN(newHueMax)) {
        // Send the value to the server
        sendCmd(`hue_max:${newHueMax}`);
    }
});
saturationMinInput.addEventListener('input', () => {
    const newsaturationMin = parseFloat(saturationMinInput.value);
    
    if (!isNaN(newsaturationMin)) {
        // Send the value to the server
        sendCmd(`saturation_min:${newsaturationMin}`);
    }
});

saturationMaxInput.addEventListener('input', () => {
    const newsaturationMax = parseFloat(saturationMaxInput.value);
    
    if (!isNaN(newsaturationMax)) {
        // Send the value to the server
        sendCmd(`saturation_max:${newsaturationMax}`);
    }
});
intensityMinInput.addEventListener('input', () => {
    const newintensityMin = parseFloat(intensityMinInput.value);
    
    if (!isNaN(newintensityMin)) {
        // Send the value to the server
        sendCmd(`intensity_min:${newintensityMin}`);
    }
});

intensityMaxInput.addEventListener('input', () => {
    const newintensityMax = parseFloat(intensityMaxInput.value);
    
    if (!isNaN(newintensityMax)) {
        // Send the value to the server
        sendCmd(`intensity_max:${newintensityMax}`);
    }
});

// WASD
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