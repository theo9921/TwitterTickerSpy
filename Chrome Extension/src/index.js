import axios from "axios";
const api = "http://localhost:3000/data/";
const errors = document.querySelector(".errors");
const loading = document.querySelector(".loading");
const i1 = document.querySelector(".i1");
const i2 = document.querySelector(".i2");
const i3 = document.querySelector(".i3");
const i4 = document.querySelector(".i4");
const results = document.querySelector(".result-container");
results.style.display = "none";
loading.style.display = "none";
errors.textContent = "";
// grab the form
const form = document.querySelector(".form-data");
// grab the country name
const handle = document.querySelector(".handle-name");

// declare a method to search by handle name
const searchForHandle = async handleName => {
  loading.style.display = "block";
  errors.textContent = "";
  try {
    const response = await axios.get(`${api}`);
    loading.style.display = "none";
    i1.textContent = toString(response.data[0].handle);
    i2.textContent = toString(response.data[0].ticker);
    i3.textContent = toString(response.data[0].fullName);
    i4.textContent = toString(response.data[0].price);
    results.style.display = "block";
  } catch (error) {
    loading.style.display = "none";
    results.style.display = "none";
    errors.textContent = "We have no data for the handle you have requested.";
  }
};

// declare a function to handle form submission
const handleSubmit = async e => {
  e.preventDefault();
  searchForHandle(handle.value);
  console.log(handle.value);
};

form.addEventListener("submit", e => handleSubmit(e));