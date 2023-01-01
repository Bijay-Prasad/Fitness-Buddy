// (A) CHANGE BMI MEASURING SYSTEM
function measureBMI () {
    // (A1) GET HTML ELEMENTS
    let unit = document.getElementById("bmi-metric").checked,
        weight = document.getElementById("bmi-weight"),
        weightu = document.getElementById("bmi-weight-unit"),
        height = document.getElementById("bmi-height"),
        heightu = document.getElementById("bmi-height-unit");
   
    // (A2) UPDATE HTML FORM FIELDS
    // TRUE = METRIC, FALSE = IMPERIAL
    if (unit) {
      weightu.innerHTML = "KG";
      weight.min = 1; weight.max = 635;
      heightu.innerHTML = "CM";
      height.min = 54; height.max = 272;
    } else {
      weightu.innerHTML = "LBS";
      weight.min = 2; weight.max = 1400;
      heightu.innerHTML = "IN";
      height.min = 21; height.max = 107;
    }
  }
   
  // (B) CALCULATE BMI
  function calcBMI () {

    
    // (B1) GET HTML ELEMENTS
    let bmi = null,
    unit = document.getElementById("bmi-metric").checked, // true = metric, false = imperial
    weight = parseInt(document.getElementById("bmi-weight").value),
    height = parseInt(document.getElementById("bmi-height").value),
    results = document.getElementById("bmi-results");
    
    // (B2) CALCULATE BMI
    // METRIC BMI = MASS (KG) / HEIGHT (M) SQUARE
    if (unit) {
      height = height / 100;
      bmi = weight / (height * height);
    }
    // IMPERIAL BMI = 703 X MASS (LBS) / HEIGHT (IN) SQUARE
    else {
      bmi = 703 * (weight / (height * height));
    }
    // ROUND OFF
    bmi = Math.round(bmi * 100) / 100; // Round off 2 decimal places
    
    document.getElementById('bmi-res').style.display = "block";
    // document.getElementById('show').style.display = "none";


    // (B3) SHOW RESULTS

    if (bmi < 18.5) {
      results.innerHTML = bmi + " - Underweight";
    } else if (bmi < 25) {
      results.innerHTML = bmi + " - Normal weight";
    } else if (bmi < 30) {
      results.innerHTML = bmi + " - Pre-obesity";
    } else if (bmi < 35) {
      results.innerHTML = bmi + " - Obesity class I";
    } else if (bmi < 40) {
      results.innerHTML = bmi + " - Obesity class II";
    } else {
      results.innerHTML = bmi + " Please enter correct value ";
    }
    return false;
  }


  ////////////////////////////////////////////////////////////////////api///////////////////////////////////////////////////////////////////////

  
    $("#search-icon").click(function() {
  $(".nav").toggleClass("search");
  $(".nav").toggleClass("no-search");
  $(".search-input").toggleClass("search-active");
});

$('.menu-toggle').click(function(){
   $(".nav").toggleClass("mobile-nav");
   $(this).toggleClass("is-active");
});




