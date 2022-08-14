// query utilities:
import {
  getByLabelText,
  getByText,
  getByTestId,
  queryByTestId,
  // Tip: all queries are also exposed on an object
  // called "queries" which you could import here as well
  waitFor,
} from '@testing-library/dom'
// adds special assertions like toHaveTextContent
import '@testing-library/jest-dom'

function getExampleDOM() {
  // This is just a raw example of setting up some DOM
  // that we can interact with. Swap this with your UI
  // framework of choice 😉
  const div = document.createElement('div')
  div.innerHTML = `
    <label for="ballername">BallerLabel</label>
    <input id="ballername" />
    <button>Print Ballername</button>
        <form onSubmit={this.handleSubmit}>
          <label>
            Calc Type:
            <select name="calc_type" value={this.state.calc_type} onChange={this.handleInputChange}>
              <option value="Blue">Blue</option>
              <option value="Green">Green</option>
              <option value="Purple">Purple</option>
              <option value="Yellow">Yellow</option>
            </select>
          </label>
          <label>
            Foo:        
             <input
            name="Foo"
            type="number"
            value={this.state.Foo}
            onChange={this.handleInputChange}  /> 
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Foo"]}</span>
          <label>
            Bar:        
             <input
            name="Bar"
            type="number"
            value={this.state.Bar}
            onChange={this.handleInputChange} /> 
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Bar"]}</span>
          <label>
            Baz:        
             <input
            name="Baz"
            type="number"
            value={this.state.Baz}
            onChange={this.handleInputChange} /> 
          <input type="submit" value="Submit" disabled={this.state.submitDisabled} />
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Baz"]}</span>
        </form>
  `
  const button = div.querySelector('button')
  const input = div.querySelector('input')
  button.addEventListener('click', () => {
    // let's pretend this is making a server request, so it's async
    // (you'd want to mock this imaginary request in your unit tests)...
    setTimeout(() => {
      const printedUsernameContainer = document.createElement('div')
      printedUsernameContainer.innerHTML = `
        <div data-testid="printed-username">${input.value}</div>
      `
      div.appendChild(printedUsernameContainer)
    }, Math.floor(Math.random() * 200))
  })
  return div
}

test('examples of some things', async () => {
  const famousBallerInHistory = 'Jordan'
  const container = getExampleDOM()

  // Get form elements by their label text.
  // An error will be thrown if one cannot be found (accessibility FTW!)
  const input = getByLabelText(container, 'BallerLabel')
  const inputTest1 = getByLabelText(container, 'Foo:')
  const inputTest2 = getByLabelText(container, 'Bar:')
  input.value = famousBallerInHistory


  // Get elements by their text, just like a real user does.
  getByText(container, 'Print Ballername').click()

  await waitFor(() =>
    expect(queryByTestId(container, 'printed-username')).toBeTruthy(),
  )

  // getByTestId and queryByTestId are an escape hatch to get elements
  // by a test id (could also attempt to get this element by its text)
  expect(getByTestId(container, 'printed-username')).toHaveTextContent(
    famousBallerInHistory,
  )



  // jest snapshots work great with regular DOM nodes!
  expect(container).toMatchSnapshot()
})