const email = document.getElementById("email").value;
const password = document.getElementById("password").value;
const btnSubmit = document.getElementById("btnSubmit")

btnSubmit.addEventListener('click', handleClick )

function handleClick(e){
  e.preventDefault();
  console.log(e);
  Login(email, password)
}


const LOGIN = ``

async function Login(email, password) {
  const formData = new FormData();
  formData.set('email', email);
  formData.set('password', password);

  const { data } = await axios.post(LOGIN, formData);
  return (data);
}