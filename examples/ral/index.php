<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RAL® color palettes</title>

    <style media="screen">
      <?php include('../examples.css') ?>
    </style>
  </head>
  <body>
    <?php
        // GLOBAL FUNCTIONS & VARIABLES
        $files = glob('../../palettes/ral/json/*/*.json');
    ?>
    <h1>RAL® color palettes</h1>

    <!-- COPYRIGHT NOTICE -->
    <header>
      RAL® and related trademarks are the property of <a href="https://www.ral-farben.de">RAL gGmbH</a> (non-profit LLC) or
      <a href="https://www.ral.de">RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V.</a>.
    </header>

    <?php include('../grid.php') ?>

    <!-- CLIPBOARD.JS -->
    <script>
      <?php include('../clipboard.js') ?>
    </script>
  </body>
</html>
<body>
