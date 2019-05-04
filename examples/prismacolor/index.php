<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Prismacolor® color palettes</title>

    <style media="screen">
      <?php include('../examples.css') ?>
    </style>
  </head>
  <body>
    <?php
        // GLOBAL FUNCTIONS & VARIABLES
        $files = glob('../../palettes/prismacolor/json/*/*.json');
    ?>
    <h1>Prismacolor® color palettes</h1>

    <!-- COPYRIGHT NOTICE -->
    <header>
      Prismacolor® and related trademarks are the property of <a href="http://www.berol.co.uk">Berol Corporation</a>,
      owned by <a href="http://www.sanfordb2b.com">Sanford L.P.</a>, a <a href="https://www.newellbrands.com">Newell Brands</a> company.
    </header>

    <?php include('../grid.php') ?>

    <!-- CLIPBOARD.JS -->
    <script>
      <?php include('../clipboard.js') ?>
    </script>
  </body>
</html>
<body>
