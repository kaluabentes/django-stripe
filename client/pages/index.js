import React, { Component } from 'react'
import Head from 'next/head'

class Home extends Component {
  state = {
    name: '',
    number: '',
    cvc: '',
    exp_month: '',
    exp_year: '',
    token: '',
  }

  handleInputChange = event => {
    this.setState({
      [event.target.name]: event.target.value,
    })
  }

  handleButtonClick = () => {
    const card = { ...this.state }
    delete card.token

    Stripe.setPublishableKey(process.env.STRIPE_PUBLISHABLE_KEY)
    Stripe.card.createToken(card, (status, response) => {
      if (response.error) {
        alert(response.error.message)
        return
      }

      this.setState({
        token: response.id,
      })
    })
  }

  render() {
    const { name, number, cvc, exp_month, exp_year, token } = this.state

    return (
      <div>
        <Head>
          <script src="https://js.stripe.com/v2/" />
        </Head>
        <input
          placeholder="Name"
          name="name"
          type="text"
          value={name}
          onChange={this.handleInputChange}
        />
        <input
          placeholder="Number"
          name="number"
          type="number"
          value={number}
          onChange={this.handleInputChange}
        />
        <input
          placeholder="CVC"
          name="cvc"
          type="number"
          value={cvc}
          onChange={this.handleInputChange}
        />
        <input
          placeholder="Exp. Month"
          name="exp_month"
          type="number"
          value={exp_month}
          onChange={this.handleInputChange}
        />
        <input
          placeholder="Exp. Year"
          name="exp_year"
          type="number"
          value={exp_year}
          onChange={this.handleInputChange}
        />
        <button onClick={this.handleButtonClick}>Pay</button>
        <div>
          Token: <pre style={{ backgroundColor: 'gray' }}>{token}</pre>
        </div>
      </div>
    )
  }
}

export default Home
