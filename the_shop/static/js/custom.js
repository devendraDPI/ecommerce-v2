// START google autocomplete field ----------------------------------------------------------------
// For optimal functionality, it is recommended to eliminate the trailing "_testremoved"
let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address_testremoved'),
    {
      types: ['geocode', 'establishment'],
      componentRestrictions: { 'country': ['in'] },
    })
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();
  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById('id_address_testremoved').placeholder = "address";
  }
  else {
    // console.log('place name=>', place.name)
  }
  // get the address components and assign them to the fields
  var geocoder = new google.maps.Geocoder()
  let address = document.getElementById('id_address').value
  geocoder.geocode({ 'address': address }, function (results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      var latitude = results[0].geometry.location.lat();
      var longitude = results[0].geometry.location.lng();
      $('#id_latitude').val(latitude);
      $('#id_longitude').val(longitude);
      $('#id_address').val(address);
    }
  });
  for (var i = 0; i < place.address_comonents.length; i++) {
    for (var j = 0; j < place.address_comonents[i].types.length; j++) {
      if (place.address_components[i].types[j] == 'country') {
        $('#id_country').val(place.address_components[i].long_name);
      }
      if (place.address_components[i].types[j] == 'administrative_area_level_1') {
        $('#id_state').val(place.address_components[i].long_name);
      }
      if (place.address_components[i].types[j] == 'locality') {
        $('#id_city').val(place.address_components[i].long_name);
      }
      if (place.address_components[i].types[j] == 'postal_code') {
        $('#id_pin_code').val(place.address_components[i].long_name);
      }
      else {
        $('#id_pin_code').val("");
      }
    }
  }
}
// END google autocomplete field ------------------------------------------------------------------


// START cart-item --------------------------------------------------------------------------------
$(document).ready(function () {
  // START increment-cart-item --------------------------------------------------------------------
  $('.increment-cart-item').on('click', function (e) {
    e.preventDefault();
    product_id = $(this).attr('data-id');
    url = $(this).attr('data-url');
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == 'signin_required') {
          Swal.fire({
            icon: 'info',
            title: 'Signin required',
            text: response.message,
          }).then(function () {
            window.location = '/account/signin';
          })
        }
        if (response.status == 'Failed') {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: response.message,
          });
        }
        else {
          $('#cart-count').html(response.cart_count['cart_count']);
          $('#quantity-' + product_id).html(response.quantity);
          if (window.location.pathname == '/cart/') {
            cartAmount(
              response.cart_amount['subtotal'],
              response.cart_amount['tax_dict'],
              response.cart_amount['total'],
            );
          }
        }
      }
    });
  });
  // START place cart item quantity on load -------------------------------------------------------
  $('.item-quantity').each(function () {
    var id = $(this).attr('id');
    var quantity = $(this).attr('data-quantity');
    $('#' + id).html(quantity);
  });
  // END place cart item quantity on load ---------------------------------------------------------
  // END increment-cart-item ----------------------------------------------------------------------
  // START decrement-cart-item --------------------------------------------------------------------
  $('.decrement-cart-item').on('click', function (e) {
    e.preventDefault();
    product_id = $(this).attr('data-id');
    url = $(this).attr('data-url');
    cart_product_id = $(this).attr('id');
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == 'signin_required') {
          Swal.fire({
            icon: 'info',
            title: 'Signin required',
            text: response.message,
          }).then(function () {
            window.location = '/account/signin';
          })
        }
        else if (response.status == 'Failed') {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: response.message,
          });
        }
        else {
          $('#cart-count').html(response.cart_count['cart_count']);
          $('#quantity-' + product_id).html(response.quantity);
          if (window.location.pathname == '/cart/') {
            removeCartElement(response.quantity, cart_product_id);
            checkEmptyCart();
            cartAmount(
              response.cart_amount['subtotal'],
              response.cart_amount['tax_dict'],
              response.cart_amount['total'],
            );
          }
        }
      }
    });
  });
  // END decrement-cart-item ----------------------------------------------------------------------
  // START delete-cart-item -----------------------------------------------------------------------
  $('.delete-cart-item').on('click', function (e) {
    e.preventDefault();
    cart_product_id = $(this).attr('data-id');
    url = $(this).attr('data-url');
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == 'Failed') {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: response.message,
          });
        }
        else {
          $('#cart-count').html(response.cart_count['cart_count']);
          Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'Success',
            text: response.message,
            showConfirmButton: false,
            timer: 1500
          })
          if (window.location.pathname == '/cart/') {
            cartAmount(
              response.cart_amount['subtotal'],
              response.cart_amount['tax_dict'],
              response.cart_amount['total'],
            );
          }
          removeCartElement(0, cart_product_id);
          checkEmptyCart();
        }
      }
    });
  });
  // END delete-cart-item -------------------------------------------------------------------------
  // START remove-cart-element if quantity is zero ------------------------------------------------
  function removeCartElement(cartItemQuantity, cart_product_id) {
    if (cartItemQuantity <= 0) {
      document.getElementById('cart-item-' + cart_product_id).remove();
    }
  }
  // END remove-cart-element if quantity is zero --------------------------------------------------
  // START check if cart is empty -----------------------------------------------------------------
  function checkEmptyCart() {
    var cart_count = document.getElementById('cart-count').innerHTML
    if (cart_count == 0) {
      document.getElementById('empty-cart').style.display = 'block';
    }
  }
  // END check if cart is empty -------------------------------------------------------------------
  // START check amount ---------------------------------------------------------------------------
  function cartAmount(subtotal, tax_dict, total) {
    $('#subtotal').html(subtotal);
    $('#total').html(total);
    for (key1 in tax_dict) {
      for (key2 in tax_dict[key1]) {
        $('#tax-' + key1).html(tax_dict[key1][key2]);
      }
    }
  }
  // END check amount -----------------------------------------------------------------------------
  // START add operating hours --------------------------------------------------------------------
  $('.add-hour').on('click', function (e) {
    e.preventDefault();
    var day = document.getElementById('id_day').value
    var from_hour = document.getElementById('id_from_hour').value
    var to_hour = document.getElementById('id_to_hour').value
    var is_closed = document.getElementById('id_is_closed').checked
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    var url = document.getElementById('add-hour-url').value
    if (is_closed) {
      is_closed = 'True'
      condition = "day != ''"
    }
    else {
      is_closed = 'False'
      condition = "day != '' && from_hour != '' && to_hour != ''"
    }
    if (eval(condition)) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          'day': day,
          'from_hour': from_hour,
          'to_hour': to_hour,
          'is_closed': is_closed,
          'csrfmiddlewaretoken': csrf_token,
        },
        success: function (response) {
          if (response.status == 'Success') {
            if (response.is_closed == 'Closed') {
              html = '<tr id="hour-' + response.id + '"><td><i class="bi bi-activity"></i></td><td><b>' + response.day + '</b></td><td><b class="text-danger">Closed</b></td><td><a href="" style="color: unset;" class="remove-hour" data-url="/account/vendor/operating-hours/remove/' + response.id + '/"><i class="bi bi-trash text-danger"></i></a></td></tr>';
            }
            else {
              html = '<tr id="hour-' + response.id + '"><td><i class="bi bi-activity"></i></td><td><b>' + response.day + '</b></td><td>' + response.from_hour + ' - ' + response.to_hour + '</td><td><a href="" style="color: unset;" class="remove-hour" data-url="/account/vendor/operating-hours/remove/' + response.id + '/"><i class="bi bi-trash text-danger"></i></a></td></tr>';
            }
            $('.operating-hours').append(html);
            document.getElementById('operating-hours').reset();
          }
          else {
            Swal.fire({
              position: 'center',
              icon: 'error',
              title: 'Error',
              text: response.message,
            })
          }
        }
      });
    }
    else {
      Swal.fire({
        position: 'center',
        icon: 'warning',
        title: 'Required',
        text: 'Day and Open/Close fields are required',
      })
    }
  })
  // End add operating hours ----------------------------------------------------------------------
  // START remove operating hours -----------------------------------------------------------------
  $(document).on('click', '.remove-hour', function (e) {
    e.preventDefault();
    url = $(this).attr('data-url');
    $.ajax({
      type: 'GET',
      url: url,
      success: function (response) {
        if (response.status == 'Success') {
          document.getElementById('hour-' + response.id).remove();
        }
      }
    })
  })
  // END remove operating hours -------------------------------------------------------------------
});
// END cart-item ----------------------------------------------------------------------------------
