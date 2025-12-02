-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-12-2025 a las 18:38:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `nutriapp_vogd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingredientes_receta`
--

CREATE TABLE `ingredientes_receta` (
  `id` int(11) NOT NULL,
  `receta_id` int(11) DEFAULT NULL,
  `ingrediente` varchar(200) DEFAULT NULL,
  `cantidad` varchar(100) DEFAULT NULL,
  `fdc_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `ingredientes_receta`
--

INSERT INTO `ingredientes_receta` (`id`, `receta_id`, `ingrediente`, `cantidad`, `fdc_id`) VALUES
(125, 2, 'Garbanzos cocidos', '150 g', NULL),
(126, 2, 'Tomate cherry', '60 g', NULL),
(127, 2, 'Pepino', '60 g', NULL),
(128, 2, 'Aceite de oliva', '15 g', NULL),
(129, 2, 'Limón', '15 g', NULL),
(130, 3, 'Tortilla integral', '40 g', NULL),
(131, 3, 'Hummus', '45 g', NULL),
(132, 3, 'Zanahoria rallada', '60 g', NULL),
(133, 3, 'Espinaca', '30 g', NULL),
(134, 4, 'Carne de soya hidratada', '120 g', NULL),
(135, 4, 'Cebolla', '30 g', NULL),
(136, 4, 'Ajo', '5 g', NULL),
(137, 4, 'Tortillas', '75 g', NULL),
(138, 5, 'Avena', '150 g', NULL),
(139, 5, 'Plátano machacado', '100 g', NULL),
(140, 5, 'Chispas de chocolate veganas', '30 g', NULL),
(141, 6, 'Harina de almendra', '100 g', NULL),
(142, 6, 'Huevo', '100 g', NULL),
(143, 6, 'Miel', '15 g', NULL),
(144, 7, 'Arroz cocido', '150 g', NULL),
(145, 7, 'Zanahoria', '30 g', NULL),
(146, 7, 'Huevo', '50 g', NULL),
(147, 7, 'Salsa soya sin gluten', '15 g', NULL),
(148, 8, 'Mango', '150 g', NULL),
(149, 8, 'Yogur natural', '120 g', NULL),
(150, 8, 'Miel', '5 g', NULL),
(151, 9, 'Quinoa', '150 g', NULL),
(152, 9, 'Pepino', '60 g', NULL),
(153, 9, 'Tomate', '60 g', NULL),
(154, 10, 'Huevo', '100 g', NULL),
(155, 10, 'Pimiento', '30 g', NULL),
(156, 10, 'Espinaca', '30 g', NULL),
(157, 11, 'Atún en agua', '140 g', NULL),
(158, 11, 'Huevo', '50 g', NULL),
(159, 11, 'Avena', '40 g', NULL),
(160, 12, 'Pechuga de pollo', '150 g', NULL),
(161, 12, 'Ajo', '5 g', NULL),
(162, 12, 'Sal', '1 g', NULL),
(163, 13, 'Jamón de pavo', '80 g', NULL),
(164, 13, 'Queso panela', '50 g', NULL),
(165, 14, 'Yogur griego', '220 g', NULL),
(166, 14, 'Proteína en polvo', '30 g', NULL),
(167, 14, 'Fresas', '30 g', NULL),
(168, 15, 'Huevo', '100 g', NULL),
(169, 15, 'Claras', '70 g', NULL),
(170, 15, 'Espinaca', '30 g', NULL),
(171, 16, 'Tostadas horneadas', '40 g', NULL),
(172, 16, 'Frijoles refritos', '120 g', NULL),
(173, 16, 'Lechuga', '30 g', NULL),
(174, 16, 'Salsa', '30 g', NULL),
(175, 17, 'Tortillas', '75 g', NULL),
(176, 17, 'Frijoles licuados', '150 g', NULL),
(177, 17, 'Queso panela', '30 g', NULL),
(178, 18, 'Arroz', '150 g', NULL),
(179, 18, 'Pollo', '100 g', NULL),
(180, 18, 'Elote', '30 g', NULL),
(181, 18, 'Pico de gallo', '60 g', NULL),
(182, 19, 'Zanahoria', '60 g', NULL),
(183, 19, 'Calabaza', '60 g', NULL),
(184, 19, 'Papa', '75 g', NULL),
(185, 19, 'Agua', '720 g', NULL),
(186, 20, 'Camarón', '200 g', NULL),
(187, 20, 'Pepino', '60 g', NULL),
(188, 20, 'Limón', '60 g', NULL),
(189, 20, 'Chile verde', '20 g', NULL),
(190, 21, 'Yogur griego', '220 g', NULL),
(191, 21, 'Miel', '15 g', NULL),
(192, 21, 'Fresas', '30 g', NULL),
(193, 22, 'Avena', '150 g', NULL),
(194, 22, 'Plátano', '100 g', NULL),
(195, 22, 'Cacao', '30 g', NULL),
(196, 23, 'Manzana', '150 g', NULL),
(197, 23, 'Canela', '5 g', NULL),
(198, 23, 'Miel', '5 g', NULL),
(199, 24, 'Gelatina sin azúcar', '7 g', NULL),
(200, 24, 'Agua', '480 g', NULL),
(201, 25, 'Yogur natural', '240 g', NULL),
(202, 25, 'Frutas picadas', '75 g', NULL),
(203, 26, 'Arroz', '150 g', NULL),
(204, 26, 'Zanahoria', '30 g', NULL),
(205, 26, 'Calabaza', '30 g', NULL),
(206, 27, 'Pasta', '150 g', NULL),
(207, 27, 'Tomate', '120 g', NULL),
(208, 27, 'Ajo', '5 g', NULL),
(209, 28, 'Atún en agua', '140 g', NULL),
(210, 28, 'Lechuga', '30 g', NULL),
(211, 28, 'Limón', '15 g', NULL),
(212, 29, 'Huevo', '100 g', NULL),
(213, 29, 'Tortillas', '50 g', NULL),
(214, 30, 'Avena', '150 g', NULL),
(215, 30, 'Agua', '240 g', NULL),
(216, 30, 'Miel', '5 g', NULL),
(217, 31, 'Pan integral', '60 g', NULL),
(218, 31, 'Jamón de pavo', '40 g', NULL),
(219, 31, 'Lechuga', '15 g', NULL),
(220, 32, 'Espinaca', '30 g', NULL),
(221, 32, 'Plátano', '100 g', NULL),
(222, 32, 'Agua', '240 g', NULL),
(223, 33, 'Avena', '150 g', NULL),
(224, 33, 'Leche', '240 g', NULL),
(225, 34, 'Pan integral', '60 g', NULL),
(226, 34, 'Aguacate', '70 g', NULL),
(227, 34, 'Limón', '5 g', NULL),
(228, 35, 'Yogur natural', '240 g', NULL),
(229, 35, 'Fresas', '30 g', NULL),
(230, 36, 'Pollo', '150 g', NULL),
(231, 36, 'Limón', '30 g', NULL),
(232, 36, 'Ajo', '5 g', NULL),
(233, 37, 'Lechuga', '30 g', NULL),
(234, 37, 'Tomate', '60 g', NULL),
(235, 38, 'Pasta', '150 g', NULL),
(236, 38, 'Tomate', '120 g', NULL),
(237, 38, 'Aceite de oliva', '5 g', NULL),
(238, 39, 'Harina', '120 g', NULL),
(239, 39, 'Huevo', '50 g', NULL),
(240, 39, 'Leche', '240 g', NULL),
(241, 40, 'Salmón', '150 g', NULL),
(242, 40, 'Limón', '15 g', NULL),
(243, 40, 'Ajo', '5 g', NULL),
(244, 41, 'huevo', '100.0', NULL),
(245, 41, 'pan', '100.0', NULL),
(246, 41, 'mantequilla', '15.0', NULL),
(247, 41, 'jugo de nranga', '15.0', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pasos_receta`
--

CREATE TABLE `pasos_receta` (
  `id` int(11) NOT NULL,
  `receta_id` int(11) NOT NULL,
  `numero_paso` int(11) NOT NULL,
  `descripcion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `pasos_receta`
--

INSERT INTO `pasos_receta` (`id`, `receta_id`, `numero_paso`, `descripcion`) VALUES
(1, 1, 1, 'Cocina la quinoa según las instrucciones.'),
(2, 1, 2, 'Mezcla con garbanzos cocidos y espinaca fresca.'),
(3, 1, 3, 'Agrega jugo de limón y sal al gusto.'),
(4, 2, 1, 'Cocina las lentejas.'),
(5, 2, 2, 'Sazónalas con especias.'),
(6, 2, 3, 'Sirve en tortillas con aguacate y pico de gallo.'),
(7, 3, 1, 'Saltea el tofu en una sartén.'),
(8, 3, 2, 'Agrega las verduras mixtas.'),
(9, 3, 3, 'Añade salsa de soya light y mezcla.'),
(10, 4, 1, 'Cocina la pasta.'),
(11, 4, 2, 'Prepara el pesto con albahaca, nuez y ajo.'),
(12, 4, 3, 'Mezcla la pasta con el pesto.'),
(13, 5, 1, 'Sofríe cebolla y especias.'),
(14, 5, 2, 'Agrega garbanzos y leche de coco.'),
(15, 5, 3, 'Cocina hasta espesar.'),
(16, 6, 1, 'Licúa avena con plátano.'),
(17, 6, 2, 'Vierte en la sartén.'),
(18, 6, 3, 'Cocina ambos lados.'),
(19, 7, 1, 'Mezcla la masa de maíz con agua.'),
(20, 7, 2, 'Amasa y forma tortillas.'),
(21, 7, 3, 'Cocina en comal.'),
(22, 8, 1, 'Cocina la pasta de arroz.'),
(23, 8, 2, 'Prepara salsa de tomate natural.'),
(24, 8, 3, 'Mezcla y sirve.'),
(25, 9, 1, 'Mezcla harinas y levadura.'),
(26, 9, 2, 'Amasa con agua tibia.'),
(27, 9, 3, 'Hornea hasta dorar.'),
(28, 10, 1, 'Prepara la masa sin gluten.'),
(29, 10, 2, 'Agrega salsa y vegetales.'),
(30, 10, 3, 'Hornea hasta crujir.'),
(31, 11, 1, 'Cocina la quinoa.'),
(32, 11, 2, 'Asa la pechuga de pollo.'),
(33, 11, 3, 'Sirve con verduras.'),
(34, 12, 1, 'Bate los huevos.'),
(35, 12, 2, 'Agrega espinaca y tomate.'),
(36, 12, 3, 'Cocina en sartén.'),
(37, 13, 1, 'Escurre el atún.'),
(38, 13, 2, 'Mezcla con pepino y limón.'),
(39, 13, 3, 'Agrega chile al gusto.'),
(40, 14, 1, 'Cocina el arroz al vapor.'),
(41, 14, 2, 'Sella el salmón.'),
(42, 14, 3, 'Sirve todo en un bowl.'),
(43, 15, 1, 'Asa el bistec.'),
(44, 15, 2, 'Corta en tiras.'),
(45, 15, 3, 'Sirve en tortillas con cebolla y cilantro.'),
(46, 16, 1, 'Cocina los nopales.'),
(47, 16, 2, 'Sirve en tortilla.'),
(48, 16, 3, 'Agrega salsa verde.'),
(49, 17, 1, 'Corta todas las verduras.'),
(50, 17, 2, 'Mezcla en un bowl.'),
(51, 17, 3, 'Agrega limón al gusto.'),
(52, 18, 1, 'Hierve agua con sal.'),
(53, 18, 2, 'Agrega las verduras.'),
(54, 18, 3, 'Cocina hasta suavizar.'),
(55, 19, 1, 'Cocina el pollo en agua.'),
(56, 19, 2, 'Agrega salsa verde.'),
(57, 19, 3, 'Cocina 10 minutos más.'),
(58, 20, 1, 'Corta pollo y vegetales.'),
(59, 20, 2, 'Saltea todo.'),
(60, 20, 3, 'Sirve caliente.'),
(61, 21, 1, 'Mezcla avena, cacao y stevia.'),
(62, 21, 2, 'Vierte en molde.'),
(63, 21, 3, 'Hornea 20 minutos.'),
(64, 22, 1, 'Prepara gelatina con agua caliente.'),
(65, 22, 2, 'Agrega proteína en polvo.'),
(66, 22, 3, 'Refrigera.'),
(67, 23, 1, 'Aplasta plátano y mezcla con avena.'),
(68, 23, 2, 'Forma galletas.'),
(69, 23, 3, 'Hornea.'),
(70, 24, 1, 'Congela plátano.'),
(71, 24, 2, 'Licúalo.'),
(72, 24, 3, 'Sirve frío.'),
(73, 25, 1, 'Mezcla ingredientes light.'),
(74, 25, 2, 'Vierte en molde.'),
(75, 25, 3, 'Hornea.'),
(76, 26, 1, 'Cocina el arroz.'),
(77, 26, 2, 'Fríe el huevo.'),
(78, 26, 3, 'Sirve junto.'),
(79, 27, 1, 'Hierve agua.'),
(80, 27, 2, 'Agrega fideos y verduras.'),
(81, 27, 3, 'Cocina por 10 minutos.'),
(82, 28, 1, 'Mezcla papa con huevo.'),
(83, 28, 2, 'Forma tortitas.'),
(84, 28, 3, 'Fríe ligeramente.'),
(85, 29, 1, 'Lava los frijoles.'),
(86, 29, 2, 'Cocínalos en olla.'),
(87, 29, 3, 'Sazona al gusto.'),
(88, 30, 1, 'Sofríe jitomate, cebolla y ajo.'),
(89, 30, 2, 'Agrega arroz.'),
(90, 30, 3, 'Cocina con agua.'),
(91, 31, 1, 'Tuesta el pan.'),
(92, 31, 2, 'Aplasta el aguacate.'),
(93, 31, 3, 'Sirve y agrega limón.'),
(94, 32, 1, 'Corta el pepino.'),
(95, 32, 2, 'Mezcla con limón.'),
(96, 32, 3, 'Agrega chile en polvo.'),
(97, 33, 1, 'Bate huevos.'),
(98, 33, 2, 'Agrega queso y espinaca.'),
(99, 33, 3, 'Cocina en sartén.'),
(100, 34, 1, 'Saltea los champiñones.'),
(101, 34, 2, 'Rellena tortillas.'),
(102, 34, 3, 'Calienta en comal.'),
(103, 35, 1, 'Mezcla atún con verduras.'),
(104, 35, 2, 'Agrega limón.'),
(105, 35, 3, 'Sirve en tortilla.'),
(106, 36, 1, 'Saltea champiñones.'),
(107, 36, 2, 'Agrega arroz y caldo.'),
(108, 36, 3, 'Cocina hasta cremoso.'),
(109, 37, 1, 'Sella el salmón.'),
(110, 37, 2, 'Agrega mantequilla y limón.'),
(111, 37, 3, 'Cocina 5 minutos.'),
(112, 38, 1, 'Abre la pechuga.'),
(113, 38, 2, 'Rellena con espinaca y queso.'),
(114, 38, 3, 'Hornea.'),
(115, 39, 1, 'Sofríe verduras.'),
(116, 39, 2, 'Agrega mariscos y arroz.'),
(117, 39, 3, 'Cocina hasta listo.'),
(118, 40, 1, 'Arma capas de verduras y queso.'),
(119, 40, 2, 'Agrega salsa.'),
(120, 40, 3, 'Hornea hasta dorar.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recetas`
--

CREATE TABLE `recetas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `dificultad` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `calorias_totales` float DEFAULT NULL,
  `proteinas` float DEFAULT NULL,
  `grasas` float DEFAULT NULL,
  `carbohidratos` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `recetas`
--

INSERT INTO `recetas` (`id`, `nombre`, `categoria`, `dificultad`, `descripcion`, `calorias_totales`, `proteinas`, `grasas`, `carbohidratos`) VALUES
(1, 'Bowl vegano de quinoa', 'Veganas', 'Principiante', 'Quinoa con garbanzos, espinaca y aderezo de limón.', NULL, NULL, NULL, NULL),
(2, 'Tacos veganos de lentejas', 'Veganas', 'Intermedio', 'Tortillas con lentejas sazonadas, aguacate y pico de gallo.', NULL, NULL, NULL, NULL),
(3, 'Ensalada tibia de tofu', 'Veganas', 'Principiante', 'Tofu salteado con verduras mixtas y salsa soya light.', NULL, NULL, NULL, NULL),
(4, 'Pasta vegana al pesto', 'Veganas', 'Intermedio', 'Pasta con pesto de albahaca, nuez y ajo.', NULL, NULL, NULL, NULL),
(5, 'Curry vegano de garbanzos', 'Veganas', 'Intermedio', 'Curry cremoso de garbanzos con leche de coco.', NULL, NULL, NULL, NULL),
(6, 'Hotcakes sin gluten de avena', 'Sin gluten', 'Principiante', 'Hotcakes hechos con avena molida y plátano.', NULL, NULL, NULL, NULL),
(7, 'Tortillas sin gluten de maíz', 'Sin gluten', 'Principiante', 'Tortillas caseras de maíz 100% natural.', NULL, NULL, NULL, NULL),
(8, 'Pasta sin gluten con tomate', 'Sin gluten', 'Intermedio', 'Pasta de arroz con salsa natural de tomate.', NULL, NULL, NULL, NULL),
(9, 'Pan sin gluten básico', 'Sin gluten', 'Experto', 'Pan casero a base de harina de arroz y almendra.', NULL, NULL, NULL, NULL),
(10, 'Pizza sin gluten', 'Sin gluten', 'Intermedio', 'Base de harina sin gluten con vegetales frescos.', NULL, NULL, NULL, NULL),
(11, 'Pollo a la plancha con quinoa', 'Alta proteína', 'Principiante', 'Pechuga de pollo acompañada de quinoa y verduras.', NULL, NULL, NULL, NULL),
(12, 'Huevos revueltos con espinaca', 'Alta proteína', 'Principiante', 'Huevos con espinaca fresca y tomate.', NULL, NULL, NULL, NULL),
(13, 'Atún con ensalada fresca', 'Alta proteína', 'Principiante', 'Lata de atún con pepino, limón y chile.', NULL, NULL, NULL, NULL),
(14, 'Bowl de arroz con salmón', 'Alta proteína', 'Intermedio', 'Arroz al vapor con salmón sellado.', NULL, NULL, NULL, NULL),
(15, 'Tacos de bistec light', 'Alta proteína', 'Intermedio', 'Tacos de bistec asado con cebolla y cilantro.', NULL, NULL, NULL, NULL),
(16, 'Tacos mexicanos de nopales', 'Mexicanas saludables', 'Principiante', 'Tacos de nopal con salsa verde.', NULL, NULL, NULL, NULL),
(17, 'Ensalada mexicana ligera', 'Mexicanas saludables', 'Principiante', 'Lechuga con jitomate, pepino y limón.', NULL, NULL, NULL, NULL),
(18, 'Sopa de verduras mexicana', 'Mexicanas saludables', 'Intermedio', 'Caldo de verduras con calabaza, zanahoria y papa.', NULL, NULL, NULL, NULL),
(19, 'Pollo en salsa verde light', 'Mexicanas saludables', 'Intermedio', 'Pollo cocido con salsa verde sin grasa.', NULL, NULL, NULL, NULL),
(20, 'Fajitas de pollo saludables', 'Mexicanas saludables', 'Principiante', 'Tiras de pollo con pimientos y cebolla.', NULL, NULL, NULL, NULL),
(21, 'Brownie fit de cacao', 'Postres fit', 'Intermedio', 'Brownie con avena, cacao y stevia.', NULL, NULL, NULL, NULL),
(22, 'Gelatina proteica', 'Postres fit', 'Principiante', 'Gelatina hecha con proteína en polvo.', NULL, NULL, NULL, NULL),
(23, 'Galletas fit de avena', 'Postres fit', 'Principiante', 'Galletas hechas con avena y plátano.', NULL, NULL, NULL, NULL),
(24, 'Helado fit de plátano', 'Postres fit', 'Principiante', 'Helado cremoso de plátano congelado.', NULL, NULL, NULL, NULL),
(25, 'Cheesecake light', 'Postres fit', 'Intermedio', 'Cheesecake reducido en azúcar y grasa.', NULL, NULL, NULL, NULL),
(26, 'Arroz con huevo económico', 'Económicas', 'Principiante', 'Arroz blanco con huevo frito.', NULL, NULL, NULL, NULL),
(27, 'Sopa económica de fideos', 'Económicas', 'Principiante', 'Caldo con fideos delgados y verduras.', NULL, NULL, NULL, NULL),
(28, 'Tortitas de papa', 'Económicas', 'Principiante', 'Puré de papa con huevo y pan molido.', NULL, NULL, NULL, NULL),
(29, 'Frijoles de la olla', 'Económicas', 'Intermedio', 'Frijoles cocidos caseros.', NULL, NULL, NULL, NULL),
(30, 'Arroz a la mexicana', 'Económicas', 'Principiante', 'Arroz con jitomate, cebolla y ajo.', NULL, NULL, NULL, NULL),
(31, 'Tostadas de aguacate', '10 minutos', 'Principiante', 'Pan tostado con aguacate y limón.', NULL, NULL, NULL, NULL),
(32, 'Ensalada fresca de pepino', '10 minutos', 'Principiante', 'Pepino con limón, sal y chile en polvo.', NULL, NULL, NULL, NULL),
(33, 'Omelette rápido', '10 minutos', 'Principiante', 'Omelette con queso y espinaca.', NULL, NULL, NULL, NULL),
(34, 'Quesadillas de champiñón', '10 minutos', 'Principiante', 'Tortillas con champiñones salteados.', NULL, NULL, NULL, NULL),
(35, 'Tacos de atún exprés', '10 minutos', 'Principiante', 'Atún en tortilla con limón y verduras.', NULL, NULL, NULL, NULL),
(36, 'Risotto de champiñones', 'Intermedio', 'Intermedio', 'Arroz cremoso con champiñones.', NULL, NULL, NULL, NULL),
(37, 'Salmón en mantequilla', 'Intermedio', 'Intermedio', 'Salmón sellado con mantequilla y limón.', NULL, NULL, NULL, NULL),
(38, 'Pechuga rellena de espinaca', 'Intermedio', 'Experto', 'Pechuga rellena con espinaca y queso.', NULL, NULL, NULL, NULL),
(39, 'Paella saludable', 'Intermedio', 'Experto', 'Paella ligera con mariscos.', NULL, NULL, NULL, NULL),
(40, 'Lasagna saludable', 'Intermedio', 'Experto', 'Lasagna de verduras con queso bajo en grasa.', NULL, NULL, NULL, NULL),
(41, 'Desayuno favorito', 'Personalizada', 'Media', 'Delicioso', 525.5, 16.9, 20.9, 67.75);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(100) UNSIGNED NOT NULL,
  `nombre` varchar(50) NOT NULL DEFAULT '0',
  `apellidos` varchar(200) NOT NULL DEFAULT '0',
  `correo` varchar(120) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `edad` int(11) NOT NULL,
  `sexo` varchar(20) NOT NULL DEFAULT '',
  `peso` float NOT NULL DEFAULT 0,
  `altura` float NOT NULL DEFAULT 0,
  `preferencias` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='usuarios registrados';

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellidos`, `correo`, `telefono`, `contrasena`, `edad`, `sexo`, `peso`, `altura`, `preferencias`) VALUES
(1, 'wendy Judith', 'vazquez ortiz', 'ivsnachote@gmail.com', '+526562057669', 'scrypt:32768:8:1$IL3yaWV34A7tfecu$a87d338c30810aa852c4ce01e8cb1caf09860cb25cec2c0cec8057c5a457df2435e4fdef298be5f69be909185c42d641dc0ff533a88cff686a8e750a0a3e4ed7', 17, 'hombre', 68, 170, '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ingredientes_receta`
--
ALTER TABLE `ingredientes_receta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receta_id` (`receta_id`);

--
-- Indices de la tabla `pasos_receta`
--
ALTER TABLE `pasos_receta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receta_id` (`receta_id`);

--
-- Indices de la tabla `recetas`
--
ALTER TABLE `recetas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ingredientes_receta`
--
ALTER TABLE `ingredientes_receta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=248;

--
-- AUTO_INCREMENT de la tabla `pasos_receta`
--
ALTER TABLE `pasos_receta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT de la tabla `recetas`
--
ALTER TABLE `recetas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(100) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ingredientes_receta`
--
ALTER TABLE `ingredientes_receta`
  ADD CONSTRAINT `ingredientes_receta_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pasos_receta`
--
ALTER TABLE `pasos_receta`
  ADD CONSTRAINT `pasos_receta_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
