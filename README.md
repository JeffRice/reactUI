Implement a React app allowing a user to monitor long-running
server-side calculations and start new ones. The calculations
continuously update their values over time (on the server) until
arriving at a final number. 

# Installation - the server

To run the server, make sure you have `python3` `pip3` 
installed.

On Mac using homebrew:
```
$ brew install python3
```

Note that Mac OS has Python 2 pre-installed, and this
server will only work with Python 3. 

In this directory, create a Python [virtualenv]() and install the
server's dependencies:

```
$ python3 -m venv venv
$ ./venv/bin/activate
$ pip install -r requirements.txt
```

Then start the server:
```
$ python3 -m server.Server
```

You can stop the server with `Ctrl-C`. The server's "database" is in
memory, but it generates data on its own periodically to simulate the
activity of other users, so restarting it will discard your running
calculations but will always provide a list of running calculations.

# The UI

The app consists of two "pages":

1) the dashboard page, on which the user sees a list of running calculations
and can start new ones. Some calculations are the user's, some are other users'.
1) a calculation detail page, on which the user can view the intermediate values
the calculation generated that led to its final value.

# Dashboard Page

The dashboard page consists of a New Calculation form and a list of
calculations under it. Calculations are either running, cancelled or
completed.

## New Calculation Form

The dashboard page lets the user start a new calculation using a form
at the top of the page.

A new calculation's inputs are:

- Calculation: the type of calculation to perform: "Blue", "Green", "Purple", or "Yellow".
- Foo: any integer from -10 to +10, inclusive
- Bar: any number
- Baz: any number from 0 to 10, inclusive

If possible, represent `Baz` with a slider component to bound the
value, but keep `Foo` and `Bar` freeform (note that `Foo` still must
be valid before submitting the form).

## Calculation List

The calculation list under the form shows a list of currently-running
and recently-run calculations, and updates the list with data from the
server once per second. 

The list lets the user watch how each calculation's value is evolving,
and also lets them see if any calculations encounter errors.

Keep in mind that other users are also launching calculations, and that
calculations will already be in progress and will have already
finished when the UI's page loads. 

Each row in the calculation list should include the following:
- the inputs of the calculation, listed above under "New Calculation Form"
- the calculation's current value 
- an indication of the calculation's progress and time remaining to completion 
  (the data from the server will include this information)
- the calculation's state - `Running`, `Cancelled`, or `Completed`.
- a "Cancel" button that notifies the server to cancel the calculation
- A "Duplicate" button that prepopulates the "New Calculation" form with that row's values.

The UI should visually distinguish the user's own calculations in the list
from those of other users, and visually flash the row when one of the user's
calculations completes.

Above the list, provide a toggle switch that toggles the list between
displaying all calculations and only this user's calculations.

Note that because the app does not include a login page or anything similar,
if the user reloads the page it will not know on reload which calculations
belong to this user. This is just a limitation of the assignment.

## Calculation Detail Page

Clicking a calculation in the list (other than its "Cancel", "Hide"
and "Duplicate" buttons) replaces the list page with a Calculation
Detail page, which displays the Calculation's inputs, and all of its
intermediate values (its `values` property) as it derived its final
value. If the calculation encountered an error, the detail page
displays the intermediate values determined before the error, and then
the error that was encountered and when it was encountered.

Note that this should not render the list component at all while the
detail page is showing. The intention is to provide an opportunity to
show how you manage the state of the calculation list component while
it's not rendered.

If you're so inspired, and curious about what the values are a product
of, you could add a visual line graph of the array of `values` as a
bonus.  They're not random; they're the y-values of mathematical
functions created from the `foo`, `bar` and `baz` inputs.

# Server endpoints

The following are the endpoints provided by the server. The requests
involving calculations represent a calculation with an object such as
the following:

```
{
  "id": "570b04b6-e88e-412a-9352-2c295b783351",
  "username": "Fred",
  "type": "Blue",
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

The `type`, `foo`, `bar` and `baz` properties
correspond to the inputs described above under "New Calculation Form"

- `id` is a unique ID generated by the server when starting a calculation
- `started_at` is the time the calculation started executing.
- `cancelled_at` is the time the user cancelled the calculation, or null.
- `completed_at` is the time the calculation finished, or null if the calculation is still running.
- `value` is the current value of the calculation as it proceeds.

If `error` is not `null`, it means the calculation encountered an
error before it could complete, and `error` will be an object
containing two properties: `errored_at` and `error`, where
`errored_at` is a datetime string, and `error` is a string of the
error that occurred.

For example:
```
"error": { 
  "errored_at": "2022-02-04 12:36:04", 
  "error": "Lost connection to sensor" 
}
```

The server provides the following endpoints:

## GET /calculations

Returns a JSON array of currently-running and recently-run
calculations to display, each of the form shown above.

## GET /calculations/<uuid>

Returns a JSON object of the calculation with ID `<uuid>`. The object will
contain an extra property, `values`, which will be the list of intermediate values
the calculation went through before arriving at its final value.

## POST /calculations 

Starts a new calculation. The content-type must be `application/json`,
and the POST data is json of the calculation to start, containing the
following fields (shown in the "calculation" object shown above):

- `type`
- `foo`
- `bar`
- `baz`

All fields are required.

This endpoint returns status 201 if it was able to start the calculation;
the response data will be the new calculation's ID.

The endpoint returns status 400 if the input was invalid, with the
reason as the text of the response body.

The UI should not allow the user to submit invalid input.

## PATCH /calculations/<id>/cancel

Cancels a running calculation and returns 200. The user can cancel any
of their own calculations. If the calculation has already finished,
errored or been cancelled, the cancel request will have no effect.

