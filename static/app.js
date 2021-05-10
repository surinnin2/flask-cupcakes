
/** generate cupcake html card given cupcakeData */

function generateCupcakeHTML(cupcake) {

    return `
        <div data-id=${cupcake.id} class="card" style="width: 18rem;">
            <img src="${cupcake.image}" class="card-img-top" alt="https://tinyurl.com/demo-cupcake">
            <div class="card-body">
                <h5 class="card-title">${cupcake.flavor}</h5>
                <p class="card-text">
                    Size: ${cupcake.size}<br/>
                    Rating: ${cupcake.rating}<br/>
                </p>
                <button class="btn btn-danger" id="deleteBtn">Delete</button>
            </div>
        </div>
    `
}

/** Axios call for getting all cupcakes */

async function getCupcakes() {
    const resp = await axios.get('http://localhost:5000/api/cupcakes')

    for (let cupcake of resp.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcake))
        $('.container').append(newCupcake)
    }

}

$('.container').on('click', '#deleteBtn', async function (e) {
    let $cupcake = $(e.target).parent()
    let cupcakeID = $cupcake.parent().attr('data-id')

    await axios.delete(`http://localhost:5000/api/cupcakes/${cupcakeID}`)
    $cupcake.parent().remove()
})

$('.cupcake-form').on('submit', async function (e) {

    e.preventDefault()

    let flavor = $('#flavor').val()
    let size = $('#size').val()
    let rating = $('#rating').val()
    let image = $('#image').val()

    const resp = await axios.post('http://localhost:5000/api/cupcakes', {
        flavor,
        rating,
        size,
        image
    })

    console.log(resp)

    let newCupcake = $(generateCupcakeHTML(resp.data.cupcake))
    $('.container').append(newCupcake)
    $('.cupcake-form').trigger('reset')

})     

$(getCupcakes);