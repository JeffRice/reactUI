# eIQ Mobility Frontend Software Engineer Take-Home Project

Thank you for taking the time to do this take-home project. We've
designed it to be fun to work on, and to provide options as to how
many features of it you implement, depending on your experience with
React and how much time you have to devote to it. If you're developing
a portfolio of work and would like to include this project, you're
also free to host the provided server online.

For this assignment, you'll implement a [React](https://reactjs.org/)
single-page-app, providing a dashboard that lets a user manage a set
of calculations running on the server. You may use any other
libraries you like in implementing it.

## The provided server

Included in this repo is a server that manages a set of long-running
calculations in an in-memory database. It provides HTTP routes letting
a client start a new calculation, cancel a running calculation, get
the current set of running calculations, and get the details of a
particular calculation. Each calculation simulates
"converging" on its final value over time, updating its
current value until it arrives as its final answer.

The server also simulates other users starting and cancelling
calculations, and simulates calculations occasionally aborting to due
a transient error like a network connection. However, you should never
see exceptions in the server log - if you do please let us know.

# The UI

The following description of the UI is broken out into bullet points,
each bullet point a potential feature you could implement. Implement as many
features as you have time for; we do not expect all candidates to
implement all of the features listed. 

It might helpful to first review the [server's routes](#server-routes) to
see what calls and data are available for the UI. The UI should
prevent the user from ever submitting data that produces an HTTP 400
status code (if the server ever produces a 500 code that's our bug -
please let us know!)

We would also love to see some tests around one or two features of the
UI, using the [React Testing
Library](https://testing-library.com/docs/react-testing-library/intro/). The
tests do not have to be comprehensive or the full gamut of tests you
would write normally, just a sample.

The UI consists of three views: a login page, a calculation dashboard
page, and a calculation detail view. 

## The login page

The login page lets the user log in and use the rest of the
app. Broken out into individual features:

- The user provides a username and password and submits it to log
in. If the provided password is correct (the only valid password is
"password"), the server will respond with a user token that must be
included in all other server calls as described under 
[server routes](#server-routes)

- The app remembers the user's token when the page is refreshed.

## The dashboard page

The dashboard page consists of a table of calculations and a form to
start a new one. Broken out into individual features:

- A table of calculations provided by the server - some running, some completed,
some cancelled, some errored. The UI sorts the list by `started_at`, such
that calculations started most recently sort to the top. 

- Above the list of running calculations, a form letting the user
start a new calculation. The details of the inputs are described 
under [Server Routes](#server-routes). The UI should not let the user
submit invalid values, and should use the most appropriate UI
component for each input.

- The table updates with data from the server once per second.

- The list visually distinguishes the current user's calculations
  from those of other users.

- The user can cancel any running calculation in the list that they started.

- The user can toggle between viewing all users' calculations
and just the ones they started themselves.

- The user can hide any rows in the list they don't want to
monitor by marking the row "Hidden". 

- A toggle component above the list, "Show hidden rows",
lets the user decide whether rows they've marked as hidden should
be rendered in the list or not. The UI should remember which rows are marked
hidden, such that turning it off will hide all rows marked hidden, turning it on
will show them, and turning it off again will hide them all again. The toggle
component should only be enabled if the user has marked any rows hidden.

- Instead of displaying a calculation's `fraction_complete` as
verbatim text or a percentage, render it as a visual progress
bar. 

- The table provides pagination. 

- The table visually distinguishes a row based on its state - running, 
completed, or errored.

- A row flashes when its calculation completes, i.e. when the latest server data 
shows the calculation is completed, and the previous server data did not.

## Calculation detail view

On the server, the calculations simulate arriving at their final value
over time by continuously updating their current value. Calling the
calculation detail route will return the same information for that
calculation as the list route does, but will include an extra
property `values`, holding all the intermediate values the calculation has
produced while "converging" on its final answer. 

Broken out into individual features:

- The user can view the detail for any calculation in the list. The
  detail view can be a third page or a modal dialog/overlay that
  temporarily obscures the list.  The detail view displays the
  calculation's inputs and a graph of the calculation's `values`
  array, rendered using
  [d3](https://www.d3-graph-gallery.com/graph/line_basic.html).

  Note that React and d3 require a bit of code to play nicely together.

- The graph updates with data from the server once per second,
letting the user watch its progression over time.

- while viewing a calculation's detail view, the user can copy/paste
  the url to send to someone, and opening the app with that URL will
  show the detail view for that calculation (pretending that the app
  is deployed to a production environment with an accessible host).

# Installing the server <a name="installing-the-server"></a>

Make sure you have `python3` and `pip3` 
installed. You'll need at least python version 3.7.

On Mac using [homebrew](https://brew.sh/):
```
$ brew install python3
```

(the `$` represents the shell's command prompt).

Note that Mac OS has Python 2 pre-installed, and this
server will only work with Python 3. When running the CLI,
for simplicity always specify `python3` instead of just `python`.

In this directory, create a Python
[virtualenv](https://docs.python.org/3/library/venv.html) and install
the server's dependencies. All commands should be run from the
project's root, i.e. the directory containing this README.md file:

```
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ python3 -m server.cli -h
```

That will create a local python environment in this directory,
install the python dependencies in the new local environment,
and run the provided CLI, displaying its help text.

## Starting the server

To start the server on port 5000:
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

The server's "database" is in memory, but it seeds the database with a
few calculations at startup, so as soon as it starts and your UI
queries it for results, it will provide calculations to display. 

Note
that it never discards a calculation from memory, so if you run the
server for a very long time you may want to restart it to reclaim
memory.


## Simulated users

Periodically as the server simulates other users' activity, 
it will output notifications like the following:
```
2022-02-11 12:35:44,250 INFO: Adding calc 1033e823-8d9a-41fc-9d13-412bb09fabe6
2022-02-11 12:35:49,248 INFO: Cancelling 1033e823-8d9a-41fc-9d13-412bb09fabe6
2022-02-11 12:35:49,252 INFO: Adding calc 98a5ae1c-a9fc-49aa-af83-bb5f175086e6
2022-02-11 12:36:00,260 INFO: Adding calc c1953050-70c4-47c9-b8e2-39580d84a45a
2022-02-11 12:36:01,248 INFO: Error: f038c704-0483-448a-ad23-6759b110a229, Radiation interference
```

## --no-auth mode

To run the server without requiring a login, you can run it with `--no-auth`:
```
$ python3 -m server.cli 5000 --no-auth
```

Also note that the `/login` route will return an HTTP 400 if the server is 
started in `--no-auth` mode.

If you have any trouble getting the server running feel free to
contact us for help. 

# Server Routes <a name="server-routes"></a> 

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
calculations to display, each of the form below:

```
{
  "id": "570b04b6-e88e-412a-9352-2c295b783351",
  "mine": False,
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

- `id` is a unique ID generated by the server when starting a calculation
- `mine` is `true` or `false`, denoting whether this user created the calculation
- `calc_type`, `foo`, `bar` and `baz` correspond to the inputs submitting by the user to start the calculation.
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
  "user_id": True,
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

## GET /calculations/<uuid>

`<uuid>` here is the value of a calculation's `id` field in the list of calculations
returned by `/calculations`.

Returns a JSON object of the calculation with ID `<uuid>`. The object
will be of the form above, and contains an extra property, `values`,
which is the list of intermediate values the calculation went
through before arriving at its current value. It is an array of 2000 numbers.

## POST /calculations 

Starts a new calculation. The content-type must be `application/json`,
and the POST data is json of the calculation to start, containing the
following fields (shown in the "calculation" object shown above):

- `calc_type`: the type of calculation to perform: `blue`, `green`, `purple`, or `yellow`
- `foo`: any integer from -10 to +10, inclusive 
- `bar`: any number 
- `baz`: any number from 0 to 10, inclusive

All fields are required. If any is invalid according to the validation
rules above this route returns a 400, and the response body will be
the reason. 

The UI should not allow the user to submit invalid input.

This endpoint returns status 201 if it was able to start the calculation;
the response data will be json of the form 

```
{ "id": "f8190cb3-8124-4372-9946-479a221662d9" }
```

where `id` is the ID of the newly created calculation, and corresponds to the `id` field of
the calculation objects in the list returned by `/calculations`.

## PATCH /calculations/<uuid>/cancel

`<uuid>` here is the value of a calculation's `id` field in the list of calculations
returned by `/calculations`.

Cancels a running calculation and returns 200. The user can cancel any
of their own calculations (or any calculation if the server was
started with `--no-auth`). If the calculation has already finished,
errored or been cancelled, the cancel request will have no effect.

# Good Luck!

We hope you enjoy developing the UI. Let us know if you run into any
issues with the server - we have tested it but let us know if you
encounter any issues with it. We look forward to reviewing your
project, and we hope it's fun to work on. Good luck!
