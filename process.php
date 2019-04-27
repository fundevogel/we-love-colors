#!/usr/bin/env php

<?php

if(!defined('DS'))  define('DS', DIRECTORY_SEPARATOR);

// See https://www.php.net/manual/en/function.hexdec.php#99478
function hex2RGB($string)
{
    $string = preg_replace("/[^0-9A-Fa-f]/", '', $string);
    $array = [];

    $color = hexdec($string);
    $array['red'] = 0xFF & ($color >> 0x10);
    $array['green'] = 0xFF & ($color >> 0x8);
    $array['blue'] = 0xFF & $color;

    return $array;
}

function generateXML(array $array, string $output)
{
    // Generating XML
    $xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><SCRIBUSCOLORS/>');

    foreach ($array as $color) {
        $RGB = hex2RGB($color['hex']);
        $name = $color['name'] !== '' ? $color['name'] : $color['code'];

        // Filling XML
        $entry = $xml->addChild('COLOR');
        $entry->addAttribute('NAME', $name);
        $entry->addAttribute('SPACE', 'RGB');
        $entry->addAttribute('R', $RGB['red']);
        $entry->addAttribute('G', $RGB['green']);
        $entry->addAttribute('B', $RGB['blue']);
    }

    // Beautifying XML
    $dom = new DOMDocument('1.0');
    $dom->preserveWhiteSpace = false;
    $dom->formatOutput = true;
    $dom->loadXML($xml->asXML());
    $dom->saveXML();
    $dom->save($output);
}


$identifiers = [
    /**
     * Pantone Color Systems - Graphics
     * Pantone Matching System - PMS
     * For more information, see https://www.pantone.com/color-systems/for-graphic-design
     * or visit their shop: https://www.pantone.com/graphics
     */
    'graphic-design' => [
        'C' => [],
        'U' => [],

        /**
         * CMYK Color Guide (Coated & Uncoated)
         * https://www.pantone.com/products/graphics/cmyk-coated-uncoated
         */
        'PC' => [],
        'PU' => [],

        /**
         * Color Bridge Set (Coated & Uncoated)
         * https://www.pantone.com/products/graphics/color-bridge-coated-uncoated
         */
        'CP' => [], // https://www.pantone.com/products/graphics/color-bridge-coated
        'UP' => [], // https://www.pantone.com/products/graphics/color-bridge-uncoated

        /**
         * Extended Gamut Coated Guide
         * https://www.pantone.com/products/graphics/extended-gamut-coated-guide
         */
        'XGC' => [],

        // TODO: Pastels & Neons (C+U), see https://www.pantone.com/products/graphics/pastels-neons
        // TODO: Metallics, see https://www.pantone.com/products/graphics/metallics-guide
    ],


    /**
     * Pantone Color Systems - Fashion
     * Fashion, Home + Interiors - FHI
     * For more information, see https://www.pantone.com/color-systems/for-fashion-design
     * or visit their shop: https://www.pantone.com/fashion-home-interiors
     */
    'fashion-design' => [
        // TODO: 'Textile Paper eXtended'
        'TPX' => [],

        // TODO: 'Textile Paper Green'
        'TPG' => [],

        // TODO: 'Textile Cotton eXtended'
        'TCX' => [],

        /**
         * Nylon Brights Set
         * https://www.pantone.com/products/fashion-home-interiors/nylon-brights-set
         */
        'TN' => [],

        /**
         * Pantone SkinTone™ Guide
         * https://www.pantone.com/products/fashion-home-interiors/pantone-skintone-guide
         */
        'SP' => [],
    ],


    /**
     * Pantone Color Systems - Product
     * Plastic Standards
     * For more information, see https://www.pantone.com/color-systems/for-product-design
     * or visit the shop: https://www.pantone.com/plastics
     */
    'product-design' => [
        'PQ' => [], // https://www.pantone.com/color-intelligence/articles/technical/did-you-know-pantone-plastics-standards-explained

        // TODO: 'Textile Cotton eXtended'
        'TCX' => [],
    ],
];

$sets = './sets';
$json = file_get_contents('./pantone.json');
$array = json_decode($json, true);

foreach ($array as $category => $colors) {
    $output = $sets . DS .  $category . ' (' . count($colors) . ' colors).xml';
    generateXML($colors, $output);
}


foreach ($identifiers as $set => $subsets) {
    $setPath = $sets . DS . 'subsets' . DS . $set;

    foreach ($array[$set] as $color) {
        $code = $color['code'];

        $firstTwo = substr($code, 0, 2);
        $firstThree = substr($code, 0, 3);
        $lastTwo = substr($code, -2);
        $lastThree = substr($code, -3);

        // Graphic Design
        if ($firstTwo == 'P ') {
            if ($lastTwo == ' C') {
                $subsets['PC'][] = $color;
                // unlink($colors[$color]);
            }

            if ($lastTwo == ' U') {
                $subsets['PU'][] = $color;
                // unlink($colors[$color]);
            }
        } else {
            if ($lastTwo == ' C') {
              $subsets['C'][] = $color;
              // unlink($colors[$color]);
            }

            if ($lastTwo == ' U') {
              $subsets['U'][] = $color;
              // unlink($colors[$color]);
            }
        }

        if ($lastThree == ' CP') {
            $subsets['CP'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == ' UP') {
            $subsets['UP'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == 'XGC') {
            $subsets['XGC'][] = $color;
            // unlink($colors[$color]);
        }


        // Fashion Design
        if ($lastThree == 'TCX') {
            $subsets['TCX'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == 'TPG') {
            $subsets['TPG'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == 'TPX') {
            $subsets['TPX'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == ' TN') {
            $subsets['TN'][] = $color;
            // unlink($colors[$color]);
        }

        if ($lastThree == ' SP') {
            $subsets['SP'][] = $color;
            // unlink($colors[$color]);
        }

        // Product Design
        if ($firstThree == 'PQ-') {
            $subsets['PQ'][] = $color;
            // unlink($colors[$color]);
        }
    }

    foreach ($subsets as $key => $value) {
        $output = $setPath . DS . $key . ' (' . count($subsets[$key]) . ' colors).xml';
        generateXML($subsets[$key], $output);
    }
}
