var apiUrl = "http://127.0.0.1:8000/"
var app = new Vue({
  el: '#app',
  data: {
    loggedIn: false,
    logInStatus: "",
    newtodo: { "completed": false, "description": "" },
    todos: [],
    username: "",
    password: "",
  },
  methods: {
    login() {
      this.logInStatus = "Logging in..."
      axios.get(apiUrl + "todos/", {
        auth: { username: this.username, password: this.password },
        crossDomain: true,
      })
        .then((response) => {
          this.loggedIn = true;
          this.logInStatus = ""
          this.todos = response.data
        })
        .catch((error) => {
          this.loggingIn = false;
          if (error.response.status === 403) {
            this.logInStatus = "Incorrect Username or Password"
          }
        })
    },
    addTodo() {
      axios.post(apiUrl + "todos/", this.newtodo, {
        auth: { username: this.username, password: this.password },
        crossDomain: true
      }).then((response) => {
        this.todos.push(response.data)
        this.newtodo = { "completed": false, "description": "" }
      });
    },
    updateTodo(todo) {
      axios.put(todo.url, todo, {
        auth: { username: this.username, password: this.password },
        crossDomain: true
      }).then((response) => {
        return axios.get(apiUrl + "todos/", {
          auth: { username: this.username, password: this.password },
          crossDomain: true,
        })
      }).then((response) => {
        this.todos = response.data
      })
    },
    deleteTodo(todourl) {
      axios.delete(todourl, {
        auth: { username: this.username, password: this.password },
        crossDomain: true
      }).then((response) => {
        return axios.get(apiUrl + "todos/", {
          auth: { username: this.username, password: this.password },
          crossDomain: true,
        })
      }).then((response) => {
        this.todos = response.data
      })
    }
  }
})