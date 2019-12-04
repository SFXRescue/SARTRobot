# Configuration file options

Configuration files contain the following options:

## `network`

`ip`

The ip address of the robot (e.g. 10.0.0.3). The WebSocket server and client will attempt to bind to this address.

It can be set to '*' to bind to any available address.

## `control`

`default_gamepad_speed`

Default gamepad speed option between 1 and 8.

`default_keyboard_speed`

Default keyboard speed option between 1 and 8.

## `motors`

`type`

Type of motor connection to use. Available options:

- `dynamixel` for Dynamixel AX-series servos
- `serial` for Sabertooth motor controllers
- `virtual` for a virtual motor connection (for testing)

`port`

Serial port to connect over (e.g. `/dev/ttyACM0`).

_Not required for virtual connection._

`baudrate`

Baudrate to connect to the specified serial port with.

_Not required for virtual connection._

`ids`

Configure Dynamixel ID assignment for each motor group. Currently only `left` and `right` groups are supported which define which servos are on the left and right side. Each group is a list, allowing for multiple motors.

_Only required for Dynamixel connection._

## `cameras`

For each camera, if the `enabled` option is set, it will be shown on the interface. The URL that the interface will attempt to load the camera stream from is defined in the `id` option. Note that these settings don't modify the Motion settings, and are meant to be set to whatever has been set in the relevant Motion config files.

## `sensors`

Each sensor will have _at least_ an `enabled` option, to enable the sensor, and a `frequency` option which defines (in seconds) how often the sensor is polled.

Some sensors will have an additional `address` option to set the I²C address.

## `debug`

`print_messages`

Print any messages received from the interface to the console.