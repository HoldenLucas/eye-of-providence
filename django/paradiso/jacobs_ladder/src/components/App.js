import React from 'react'
import ReactDOM from 'react-dom'
import DataProvider from './DataProvider'
import Table from './Table'

// TODO: fix endpoint name
const App = () => (
  <DataProvider endpoint='api/guest/'
    render={data => <Table data={data} />} />
)

const wrapper = document.getElementById('app')

wrapper ? ReactDOM.render(<App />, wrapper) : null
