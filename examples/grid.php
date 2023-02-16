<?php
    /**
     * Slugifies strings (quick & dirty)
     *
     * See https://stackoverflow.com/a/34244525
     *
     * @param string $string Unslugified string
     * @return string Slugified string
     */
    function slugify(string $string): string
    {
        return strtolower(trim(preg_replace('/[^A-Za-z0-9-]+/', '-', $string)));
    }

    function str2title(string $string): string
    {
        return ucwords(str_replace('-', ' ', $string));
    }


    # Load color palettes
    $json = file_get_contents($file);
    $sets = json_decode($json, true);
?>

<!-- TABLE OF CONTENTS -->
<?php
    echo '<ul>';
    foreach (array_keys($sets) as $title) :
?>
    <li>
      <a href="#<?= slugify($title) ?>"><?= str2title($title) ?></a>
    </li>
<?php
    endforeach;
    echo '</ul>';
?>

<!-- GRID -->
<?php foreach ($sets as $title => $set) : ?>
<h2 id="<?= slugify($title) ?>">
  <?= str2title($title) ?> - <a href="#">Back to top &uarr;</a>
</h2>
<?php
    echo '<div class="grid">';

    foreach ($set as $color) :
    $name = $color['name'] !== '' ? $color['name'] : $color['code'];
?>
<div
    class="grid_item"
    style="background-color: <?= $color['hex'] ?>"
    data-clipboard-text="<?= $color['hex'] ?>"
>
    <h3><?= $name ?></h3>
</div>
<?php
    endforeach;
    echo '</div>';
?>
<?php endforeach ?>
