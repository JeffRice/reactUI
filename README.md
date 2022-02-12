eIQ Mobility Frontend Software Engineer Take-Home Project

Thank you for taking the time to do this take-home project.  We've
designed it to hopefully be fun to work on, and to provide a
number of options as to how many features of it you implement, depending
on your experience with React and how much time you have to devote to it.

For this assignment, you'll implement a [React](https://reactjs.org/)
single-page-app, providing a dashboard that lets a user manage a set
of calculations running on the server. When you submit your project,
please include instructions on how to run it, and let us know which
features you implemented.

Included in this repo is a server that manages a set of
long-running calculations. It provides HTTP routes letting 
a client start a new calculation, cancel a running calculation,
get the current set of running calculations, and get the details
of a particular calculation, including the values it has calculated so far
as it derives its final value. 

The server also simulates other users running and cancelling their own
calculations, and simulates random occasional errors.

See the section [Installing the server](#installing-the-server)
for instructions on running the server, 
and the section [Server Routes](#server-routes), for details
of its HTTP API.

Also, as you read through the description of the UI, note that you can
start the server with a `--no-auth` option, which will let the client
call its routes without a user token, though one of the potential
features to implement is a login form which will provide that token.

# The UI

The following are all potential features of this app's UI, implemented
as a single-page React app. None of these features is intended to be
particularly tricky for an expert React developer, but for a less
experienced React developer might require a bit of googling and
learning. Implement as many features as you have time for - we do not
expect all candidates to implement all of the features below.

If time allows, we would also love to see tests,
using the [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/), 
around one or two of the features implemented.

## Features

A menu of features to implement:

- A login form with username and password.

- A dashboard page that queries the server for the current set of
running calculations and displays them in a list, described in more 
detail in a section below.

- The dashboard list continuously updates by querying the server
once per second. 

- The user can submit a new calculation that then displays in the list
(if the dashboard is updating once per second, the new one
can just show up in the list on the next poll).

- The list visually distinguishes a row by its current state, one
of "Running", "Completed", "Cancelled", or "Errored" (each row should also
include its state as text).

- The list visually distinguishes calculations started by the current user
and those started by other users.

- The user can toggle whether they see all calculations in the list
or just their own, using a toggle switch component.

- The user can cancel a calculation, stopping it running on the server.

- The user can hide a calculation from view.

- The user can toggle a switch to show all hidden calculations, and then
toggle it again to hide them again (without reselecting which to
hide).

- A row flashes when its calculation completes.

- The UI remembers the user's login token when they refresh the page.

- The UI remembers the set of hidden calculations when the user refreshes the page.
  
- Clicking a calculation goes to a detail page, or displays a modal
dialog, displaying that calculation's detail view. The detail view
displays the calculation's inputs, and its intermediate values
calculated up to the current time as a graph, for example a linechart
rendered using
[d3](https://www.d3-graph-gallery.com/graph/line_basic.html).  Note
that React and d3 require a bit of code to play nicely
together. 

- The calculation detail view queries the server once per second,
updating the graph and letting the user watch its progress.

## New Calculation Form

The dashboard page lets the user start a new calculation using a form,
either at the top of the page or in a modal dialog.

A new calculation's inputs are:

- Calculation: the type of calculation to perform: "Blue", "Green", "Purple", or "Yellow"
- Foo: any integer from -10 to +10, inclusive (either a slider component or validated text field)
- Bar: any number (a text field and validaiton that the user enters a valid number)
- Baz: any number from 0 to 10, inclusive, (a slider component or a validated text field)

## The Calculation List

Each row in the calculation list should include the following:

- the inputs of the calculation, listed above under "New Calculation Form"
- the calculation's current value 
- an indication of the calculation's progress (a progress bar or text percentage)
- the calculation's state, one of `Running`, `Cancelled`, or `Completed`.
- a "Cancel" button that notifies the server to cancel the calculation
- a "Hide" button that toggles the row's inclusion in the user's hidden calculation list

## Calculation Detail 

Clicking a calculation in the list (other than its "Cancel" and "Hide"
buttons) displays the calculation's `values` list, as a list or graph,
ideally updating it once per second with data from the server.

# Installing the server 

The server is a python 
[flask](https://flask.palletsprojects.com/en/2.0.x/) app wrapped in a CLI, 
and the CLI that starts the server takes some command-line options letting 
you control aspects of the other simulated users, in case you find that useful
while debugging your app. It also provides a `'--no-auth` option,
which will let the UI call the server routes without a login.

To run the server, make sure you have `python3` and `pip3` 
installed. You'll need at least pyton version 3.7.

On Mac using [homebrew](https://brew.sh/):
```
$ brew install python3
```

(the `$` represents the shell's command prompt).

Note that Mac OS has Python 2 pre-installed, and this
server will only work with Python 3. When running the server,
for simplicity always specify `python3` instead of just `python`

In this directory, create a Python
[virtualenv](https://docs.python.org/3/library/venv.html) and install
the server's dependencies. All commands should be run from the
project's root, i.e. the directory containing this README.md file.

```
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

That will create a local python environment in this directory,
and will install the python dependencies in the new local environment.
It will not install anything globally on your computer.

Then, to start the server on port 5000:
```
$ python3 -m server.cli 5000
```

If you get an error that that address is in use, Ctrl-C a couple times
to kill the server's background processes and try again with a
different port number.

When the server starts, you should see output like the following, as
the server starts an HTTP server listening on port `5000` and starts
simulating other users creating and cancelling their own calculations:
```
2022-02-11 12:35:36,243 INFO: Simulating errors roughly every 30 seconds
2022-02-11 12:35:36,244 INFO: Simulating other users cancelling calculations roughly every 10 seconds.
2022-02-11 12:35:36,244 INFO: Simulating other users starting calculations roughly every 5 seconds.
2022-02-11 12:35:36,246 INFO: Seeding machine with 5 running calculations.
2022-02-11 12:35:36,246 INFO: Adding calc f038c704-0483-448a-ad23-6759b110a229
2022-02-11 12:35:36,246 INFO: Adding calc d870d2bf-202b-4251-b3dd-70cacc430ec4
2022-02-11 12:35:36,247 INFO: Adding calc a37cf4f9-8d28-4c25-9376-1b49c161b667
2022-02-11 12:35:36,247 INFO: Adding calc ebda0b12-15cd-481e-aef9-598fad2a3e41
2022-02-11 12:35:36,247 INFO: Adding calc 2cfd744d-156a-42a2-a9f5-4f61b8bd80b8
 * Serving Flask app 'server.server' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2022-02-11 12:35:36,254 INFO:  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
and then, periodically as the server simulates other users' activity, 
it will output notifications like the following:
```
2022-02-11 12:35:44,250 INFO: Adding calc 1033e823-8d9a-41fc-9d13-412bb09fabe6
2022-02-11 12:35:49,248 INFO: Cancelling 1033e823-8d9a-41fc-9d13-412bb09fabe6
2022-02-11 12:35:49,252 INFO: Adding calc 98a5ae1c-a9fc-49aa-af83-bb5f175086e6
2022-02-11 12:35:55,257 INFO: Adding calc f50b22e7-e26f-4a54-a77f-89259e982d60
2022-02-11 12:36:00,260 INFO: Adding calc c1953050-70c4-47c9-b8e2-39580d84a45a
2022-02-11 12:36:01,248 INFO: Error: f038c704-0483-448a-ad23-6759b110a229, Radiation interference
2022-02-11 12:36:02,249 INFO: Cancelling 1033e823-8d9a-41fc-9d13-412bb09fabe6
2022-02-11 12:36:07,254 INFO: Cancelling b8ab0f92-10dd-47c8-b214-5551fc46eab4
2022-02-11 12:36:07,265 INFO: Adding calc 01fdd296-4e91-48ab-bc9e-45c98f52db0b
```

You can stop the server with a couple `Ctrl-C`s. The server's "database" is in
memory, but it seeds the database with a few calculations at startup,
so as soon as it starts and your UI queries it for results, it will provide
calculations to display.

To control the simulated users' behavior to facilitate debugging,
e.g. speed them up, slow them down, turn them off, and to turn off the
simulatederrors, you can provide command-line switches. To see the
CLI's command-line options, do: 
``` 
$ python3 -m server.cli -h 
```
That will display help output.

For example, to turn off all simulated user behavior:
```
$ python3 -m server.cli --other-other-freq=-1
```

If you have any trouble getting the server running feel free to
contact us for help.

# Server Routes

The requests involving calculations will represent a calculation with an
object such as the following:

```
{
  "id": "570b04b6-e88e-412a-9352-2c295b783351",
  "user_id": "d842eb0f-6c8a-4a6c-8af7-f6a4f41cdc24",
  "calc_type": "Blue",
  "foo": -3,
  "bar": 6,
  "baz": -14.3,
  "value": 2.63,
  "error": null,
  "started_at": "2022-02-04 12:34:45",
  "cancelled_at": null,
  "completed_at": "2022-02-04 12:38:05"
}
```

Note that if you start the server with `--no-auth`, the calculations
will not include a `user_id` property.

- `id` is a unique ID generated by the server when starting a calculation
- `calc_type`, `foo`, `bar` and `baz` correspond to the inputs described
above under "New Calculation Form".
- `started_at` is the time the calculation started executing.
- `cancelled_at` is the time the user cancelled the calculation, or null.
- `completed_at` is the time the calculation finished, or null if the calculation is still running,
was cancelled, or encountered an error.
- `value` is the current value of the calculation as it proceeds.

If `error` is not `null`, it means the calculation encountered an
error before it could complete, and `error` will be an object
containing the type of error and when it occurred.

For example:
```
{
  "id": "570b04b6-e88e-412a-9352-2c295b783351",
  "user_id": "d842eb0f-6c8a-4a6c-8af7-f6a4f41cdc24",
  "calc_type": "Blue",
  "foo": -3,
  "bar": 6,
  "baz": -14.3,
  "value": 2.63,
  "error": { 
    "errored_at": "2022-02-04 12:36:04", 
    "error": "Lost connection to sensor" 
  },
  "started_at": "2022-02-04 12:34:45",
  "cancelled_at": null,
  "completed_at": null
}
```

The server provides the following endpoints:

## POST /login

The content-type should be `application/json`, and the POST data
is of the form:
```
{ "username": "fred", "password": "password" }
```

The only valid password is "password". Returns an HTTP 401 for an invalid password.

For a valid password, returns HTTP 200 and the json response:
```
{ "token": "f8190cb3-8124-4372-9946-479a221662d9" }
```
containing the user's session token. All subsequent requests must include
that token as an `x-auth` header.

Note that if you start the server with the option `--no-auth`,
the `/login` route will return an HTTP 400, and all other
routes will not require the `x-auth` header.

## GET /calculations

Returns a JSON array of currently-running and recently-run
calculations to display, each of the form shown above.

## GET /calculations/<uuid>

Returns a JSON object of the calculation with ID `<uuid>`. The object
will beof the form above, and contain an extra property, `values`,
which is the list of intermediate values the calculation went
through before arriving at its current value.

## POST /calculations 

Starts a new calculation. The content-type must be `application/json`,
and the POST data is json of the calculation to start, containing the
following fields (shown in the "calculation" object shown above):

- `calc_type`
- `foo`
- `bar`
- `baz`

All fields are required.

This endpoint returns status 201 if it was able to start the calculation;
the response data will be json of the form 
```
{ "id": "f8190cb3-8124-4372-9946-479a221662d9" }
```

The endpoint returns status 400 if the input was invalid, with the
reason as the text of the response body.

The UI should not allow the user to submit invalid input.

## PATCH /calculations/<id>/cancel

Cancels a running calculation and returns 200. The user can cancel any
of their own calculations (or any calculation if the server was
started with `--no-auth`). If the calculation has already finished,
errored or been cancelled, the cancel request will have no effect.

