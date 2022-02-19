import React, { Component } from 'react'

export default class Textbox extends Component {
    constructor(props) {
        super(props);
        this.state = {
          value: 'Please write an essay about your favorite DOM element.'
        };
    
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
      }
    
    handleSubmit(event) {
        alert("The rant was submitted")
        event.preventDefault()
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
            <label>
            Rant:
            <textarea value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
        </form>
        )
    }
}
