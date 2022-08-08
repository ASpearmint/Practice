var csrftoken = Cookies.get('csrftoken')

async function following(name, page) {

  if (page == undefined) {
    page = 1
  }

  const request = new Request(
    
    `/${name}/following/${page}`,
    {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  );

  let root = ReactDOM.createRoot(
    document.getElementById("following_")
  )
  let groot = ReactDOM.createRoot(
    document.getElementById("groot")
  )
  
  //For each name returned by following post their comments ordered by timestamp
  await fetch(request)
  .then( response => response.json())
  .then( data => {

    //TODO these are functions, if method doesnt work send two dict items with different maps then create two functions and call em in render
    function Create_Post() {

       let webpage = data.pages.map(content => 
          <div key={content.id+"1"}>
            <div key={content.id+"content"} className="content" onClick={() => window.location.href = `/profile/${content.person.name}`} id={content.id}> 
              <p key={content.id+content.person.name}>{content.person.name} {content.text} {content.timestamp}</p>
              <p key={content.id+content.likes} id={(content.id)+"likes"}>Likes: {content.likes}</p>
            </div>
            <div key={content.id+"2"}>
              <button key={content.id+"btn-like"} id={(content.id)+"btn-like"} onClick={() => func_like(content.id, content.likes)}>Like</button>
              <button key={content.id+"btn-unlike"} id={(content.id)+"btn-unlike"} onClick={() => func_unlike(content.id, content.likes)}>Dislike</button>
              <button key={content.id+"follow"} id={(content.id)+"btn-post"} className={content.person.name == username ? "none" : "block"} onClick={() => func_follow(content.person.name)}>Follow</button>
            </div>
          </div>

    
          );

    return (
      <div>
        {webpage}
      </div>

    );
    }

    function Paginator_3000() {
      let num_page = data.number;
      let total = [];
      
      function Content(page) {
        return (<li className="page-item"><a className="page-link" id={page} href="#" onClick={() => func_page(num_page, page)}>{page}</a></li>)
      }

      for (let i = 1; i <= num_page; i++) {
        total.push(Content(i));
      }
      

      return (<ul className="pagination" id="pagination">{total}</ul>);
    }

      root.render(<Create_Post/>);
      groot.render(<Paginator_3000/>);
      })

      .catch(error => console.error(error));

      function func_page(number, page) {
        for (let i = 1; i >= number + 1; i++) {
          $(`#${i}`).siblings.attr("class", "page-link")
        }
        $(`#${page}`).attr("class", "page-link active");
        following(name, page);
      }
}



async function profile(name) { 
  const request = new Request(
    
    `/profile/${name}`,
    {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  );

  let root = ReactDOM.createRoot(
    document.getElementById("comments")
  )
  
  
await fetch(request)
  .then( response => response.json())
  .then( data => {
    function Create_Post() {

      function handleSubmit(event) {
        event.preventDefault();
      }
    
      data = data.map(content => 
        <div key={content.id+"1"}>
          <div key={content.id+"content"} className="content" onClick={() => window.location.href = `/profile/${content.person.name}`} id={content.id}> 
            <p key={content.id+content.person.name}>{content.person.name} {content.text} {content.timestamp}</p>
            <p key={content.id+content.likes} id={(content.id)+"likes"}>Likes: {content.likes}</p>
          </div>
          <div key={content.id+"2"}>
            <button key={content.id+"btn-like"} id={(content.id)+"btn-like"} onClick={() => func_like(content.id, content.likes)}>Like</button>
            <button key={content.id+"btn-unlike"} id={(content.id)+"btn-unlike"} onClick={() => func_unlike(content.id, content.likes)}>Dislike</button>
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
    });
  }


function edit(id) {
  let data = JSON.stringify({edit : $(`#${id}form`).serialize()})
  $.post({ url: `/edit/${id}`, data : data, headers : {'X-CSRFToken': csrftoken}});
    
}

function func_follow(name) {
  fetch(`/${name}/following/0`, {
    method: 'POST', 
    headers: {'X-CSRFToken': csrftoken},
  })
  //turn button different color
  $("#btn-post").on("click", function() {
    $this.css("background-color", "red");
  });
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

