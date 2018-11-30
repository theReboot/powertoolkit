var gulp = require("gulp");
var browserSync = require("browser-sync").create();
var sass = require("gulp-sass");
var cleanCSS = require("gulp-clean-css");
var rename = require("gulp-rename");
var exec = require("child_process").exec;

// Compile sass into css
gulp.task("sass", function() {
  return gulp
    .src("devstatic/scss/*.scss")
    .pipe(sass())
    .pipe(gulp.dest("devstatic/css"))
    .pipe(
      browserSync.reload({
        stream: true
      })
    );
});

// Minify compiled CSS
gulp.task("minify-css", ["sass"], function() {
  return gulp
    .src("devstatic/css/creative.css")
    .pipe(
      cleanCSS({
        compatibility: "ie8"
      })
    )
    .pipe(
      rename({
        suffix: ".min"
      })
    )
    .pipe(gulp.dest("devstatic/css"))
    .pipe(
      browserSync.reload({
        stream: true
      })
    );
});

// Run django server
gulp.task("runserver", function() {
  var proc = exec("python manage.py runserver");
});

gulp.task("browserSync", ["runserver"], function() {
  browserSync.init({
    notify: false,
    port: 8000,
    proxy: "localhost:8000"
  });
});

gulp.task("default", ["browserSync", "sass", "minify-css"], function() {
  gulp.watch("devstatic/scss/**/*.scss", ["sass"]);
  // gulp.watch("css/*.css", ["minify-css"]);
  gulp.watch("devstatic/js/**/*.js", browserSync.reload);
  gulp.watch("templates/**/*.html", browserSync.reload);
});
