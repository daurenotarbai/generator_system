const nameInput = document.querySelector('#name_schema')
// const columnItems =document.querySelector('#columnItems')
const columnType = document.querySelector('#column_type')
const intFromDiv = document.querySelector('.intFromDiv')
const intToDiv = document.querySelector('.intToDiv')
const sentencesNumberDiv = document.querySelector('.sentencesNumberDiv')
const order = document.querySelector('#orderId')
const intFrom = document.querySelector('#intFromId')
const intTo = document.querySelector('#intToId')
const sentencesNumber = document.querySelector('#sentencesNumber')
const columnItem = document.querySelector('.column-item')
const submitBtn = document.querySelector('#submit_btn')


if(columnType.value=="full_name"){
    intFromDiv.style.display = "none"
    intToDiv.style.display = "none"
    sentencesNumberDiv.style.display = "none"
}

columnType.addEventListener('change', () => {
    if (columnType.value!="int"){
        intFromDiv.style.display = "none"
        intToDiv.style.display = "none"
}
    else {
        intFromDiv.style.display = "block"
        intToDiv.style.display = "block"
    }
    if (columnType.value!="text"){
        sentencesNumberDiv.style.display = "none"
}
    else {
        sentencesNumberDiv.style.display = "block"
    }
})

columnType.value

let arr = []
console.log(arr)

const addPerson = () => {
    const data = {
        'name':nameInput.value,
        'columnType':columnType.value,
        'intFrom':intFrom.value,
        'intTo':intTo.value,
        'sentencesNumber':sentencesNumber.value,
        'order':order.value
    }

    arr.push(data)

    let mapped = arr.map(item => {
        return `
        <div class="row">
              <div class="form-group col-lg-3">
                <label for="exampleInputEmail1">Name</label>
                <input class="form-control"  value="${item.name}"  name="name_column">
              </div>
                <div class="form-group col-lg-3">
                    <label for="exampleFormControlSelect1">Column type</label>
                    <input class="form-control" value="${item.columnType}"  name="column_type" >
                </div>
                <div class="form-group col-lg-1">
                    <label for="exampleFormControlSelect1">From</label>
                    <input type="number"  class="form-control" value="${item.intFrom}" name="int_from" >
                </div>
                <div class="form-group col-lg-1">
                    <label for="exampleFormControlSelect1">To</label>
                    <input type="number"  class="form-control" value="${item.intTo}" name="int_to">
                </div>
                <div class="form-group col-lg-1"  >
                    <label style="font-size: 8px" for="exampleFormControlSelect1">Sentences number</label>
                    <input type="number"  value="${item.sentencesNumber}" class="form-control" name="sentences_number">
                </div>
                <div class="form-group col-lg-3">
                <label for="exampleInputEmail1">Order</label>
                <input type="number"  value="${item.order}" class="form-control" name="order">
                </div>
            </div>
        `
    })
    columnItem.innerHTML = mapped.join('')
    nameInput.value = ""
    order.value = order
}


submitBtn.addEventListener('click', addPerson)

