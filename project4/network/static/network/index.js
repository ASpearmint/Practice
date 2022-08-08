var csrftoken = Cookies.get('csrftoken')

$("#submit-index").off('click').on("click", () => {
  $.post('/posts', $("#compose-form").serialize())
  $("#body").val('');
  });


//In future make it update every minute
$(window).on("load", async function() {
  const request = new Request(
    '/posts',
    {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  );

  let root = ReactDOM.createRoot(
    document.getElementById("index_")
  )
  
  
  //Possible way to do Edit page is to have previous fetch to see if request.user.username is the poster, then in Create_Post 
  //Use that true or false statement to insert button for editing

  await fetch(request)
  .then( response => response.json())
  .then( data => {
    function Create_Post() {
  
      function handleSubmit(event) {
        event.preventDefault();
      }
//TODO talk about with dillon, func_if(content.person.name) [object Promise]
      data = data.map(content => 
        <div key={content.id+"1"}>
          <div key={content.id+"content"} className="content" onClick={() => window.location.href = `/profile/${content.person.name}`} id={content.id}> 
            <p key={content.id+content.person.name}>{content.person.name} {content.text} {content.timestamp}</p>
            <p key={content.id+content.likes} id={(content.id)+"likes"}>Likes: {content.likes}</p>
          </div>
          <div key={content.id+"2"}>
            <button key={content.id+"btn-like"} id={(content.id)+"btn-like"} onClick={() => func_like(content.id, content.likes)}>Like</button>
            <button key={content.id+"btn-unlike"} id={(content.id)+"btn-unlike"} onClick={() => func_unlike(content.id, content.likes)}>Dislike</button>
            <button key={content.id+"follow"} id={(content.id)+"btn-post"} className={content.person.name == username ? "none" : "block"} onClick={() => func_follow(content.person.name)}>Follow</button>
            <form key={content.id+"form"} id={(content.id)+"form"} onSubmit={handleSubmit} className={content.person.name == username ? "block" : "none"}>
              <textarea key={content.id+"area"} id="edit" name="edit"></textarea>
              <button key={content.id+"submit"} onClick={() => edit(content.id)} type="submit">Submit</button>
            </form>
          </div>
        </div>

          
      );

      return (
        <div>
          {data}
        </div>

      );
      }

      root.render(<Create_Post/>);
  })
  .catch(error => console.error(error));
});

function edit(id) {
  let data = JSON.stringify({edit : $(`#${id}form`).serialize()})
  $.post({ url: `/edit/${id}`, data : data, headers : {'X-CSRFToken': csrftoken}});
    
}


function func_like(id, num) {
  fetch(`/like/${id}`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
  })
  //Change button color using class
  $(`#${id}btn-like`).css("background-color", "green");
  $(`#${id}likes`).html("Likes:" + (parseInt(num+1)));
  
} 

function func_unlike(id, num) {
  fetch(`/like/${id}`, {
    method: 'GET',
    headers: {'X-CSRFToken': csrftoken},
  })
  //Change button color using class
  $(`#${id}btn-unlike`).css("background-color", "red");
  $(`${id}#likes`).html("Likes:" + (parseInt(num-1)));
}

