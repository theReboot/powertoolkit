var gulp = require("gulp");
var browserSync = require("browser-sync").create();
var sass = require("gulp-sass");
var cleanCSS = require("gulp-clean-css");
var rename = require("gulp-rename");
var exec = require("child_process").exec;
var uglify = require('gulp-uglify');
var pump = require('pump');

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

// minify javascript
gulp.task('compress', function (cb) {
  pump([
        gulp.src('devstatic/js/src/main.js'),
        uglify(),
        gulp.dest('devstatic/js/dist/')
    ],
    cb
  );
});

// // Run django server
// gulp.task("runserver", function() {
//   var proc = exec("python manage.py runserver");
// });

// gulp.task("browserSync", ["runserver"], function() {
//   browserSync.init({
//     notify: false,
//     port: 8000,
//     proxy: "localhost:8000"
//   });
// });

gulp.task("default", ["sass", "minify-css", "compress"], function() {
  gulp.watch("devstatic/scss/**/*.scss", ["sass"]);
  // gulp.watch("css/*.css", ["minify-css"]);
  gulp.watch("devstatic/js/**/*.js", ["compress"]);
  // gulp.watch("devstatic/js/**/*.js", browserSync.reload);
  // gulp.watch("templates/**/*.html", browserSync.reload);
});
