import React from 'react'
import ReactDOM from 'react-dom'
import DataProvider from './DataProvider'
import Table from './Table'

import GuestCard from './GuestCard'

const App = () => (
  <DataProvider endpoint='api/guest/' render={data => <Table data={data} />} />
  // <GuestCard />
)

const wrapper = document.getElementById('app')

wrapper ? ReactDOM.render(<App />, wrapper) : null
