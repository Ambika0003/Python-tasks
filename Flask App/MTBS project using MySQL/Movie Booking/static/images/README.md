# Local images for CineBook

Put your downloaded images here (no URLs needed in the admin form).

## Movie poster

For movie ID **1**, save your poster as:

```
static/images/movies/1/poster.png
```

Supported formats: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`

You can also use `image1.png` in the same folder:

```
static/images/movies/1/image1.png
```

Or a flat file:

```
static/images/posters/1.png
```

## Cast / crew photo

For movie ID **1** and cast member ID **3** (see Admin → Edit movie → cast list):

```
static/images/movies/1/cast/3/photo.png
```

Or without a subfolder:

```
static/images/movies/1/cast/3.png
```

Using **display order** instead of cast ID (e.g. order `1` for the first actor):

```
static/images/movies/1/cast/1/photo.png
```

## Tips

1. Find the movie ID in the admin movies list or in the URL: `/movies/1` → ID is `1`.
2. After adding a cast member in admin, note their **cast ID** or **display order** for the filename.
3. Restart the browser with a hard refresh (Ctrl+F5) if an old image is cached.
