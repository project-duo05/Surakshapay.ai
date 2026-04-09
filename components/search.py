def get_animated_search_html():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background: transparent;
            margin: 0;
            padding: 5px 0 0 0;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            height: 100%;
        }

        ::selection {
            background: rgba(0, 0, 0, 0.1);
        }

        .search-wrapper {
            position: relative;
            display: flex;
            justify-content: center;
            width: 100%;
            max-width: 60px;
            transition: max-width 0.5s cubic-bezier(0.000, 0.105, 0.035, 1.570);
        }

        .search-wrapper.active {
            max-width: 100%;
        }

        .search-wrapper .input-holder {
            height: 60px;
            width: 60px;
            overflow: hidden;
            background: rgba(255, 255, 255, 0);
            border-radius: 30px;
            position: relative;
            transition: all 0.3s ease-in-out;
        }

        .search-wrapper.active .input-holder {
            width: calc(100% - 40px);
            border-radius: 30px;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all .5s cubic-bezier(0.000, 0.105, 0.035, 1.570);
        }

        .search-wrapper .input-holder .search-input {
            width: 100%;
            height: 60px;
            padding: 0px 60px 0 20px;
            opacity: 0;
            position: absolute;
            top: 0px;
            left: 0px;
            background: transparent;
            box-sizing: border-box;
            border: none;
            outline: none;
            font-family: inherit;
            font-size: 16px;
            font-weight: 500;
            color: #1e293b;
            transform: translate(0, 60px);
            transition: all .3s cubic-bezier(0.000, 0.105, 0.035, 1.570);
            transition-delay: 0.3s;
        }

        .search-wrapper.active .input-holder .search-input {
            opacity: 1;
            transform: translate(0, 0px);
        }

        .search-wrapper .input-holder .search-icon {
            width: 60px;
            height: 60px;
            border: none;
            border-radius: 30px;
            background: transparent;
            padding: 0px;
            outline: none;
            position: relative;
            z-index: 2;
            float: right;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        .search-wrapper.active .input-holder .search-icon {
            width: 44px;
            height: 44px;
            margin: 8px;
            border-radius: 22px;
            background: #0f52ba;
        }

        .search-wrapper .input-holder .search-icon span {
            width: 22px;
            height: 22px;
            display: inline-block;
            vertical-align: middle;
            position: relative;
            transform: rotate(45deg);
            transition: all .4s cubic-bezier(0.650, -0.600, 0.240, 1.650);
        }

        .search-wrapper.active .input-holder .search-icon span {
            transform: rotate(-45deg);
        }

        .search-wrapper .input-holder .search-icon span::before,
        .search-wrapper .input-holder .search-icon span::after {
            position: absolute;
            content: '';
        }

        .search-wrapper .input-holder .search-icon span::before {
            width: 4px;
            height: 12px;
            left: 9px;
            top: 15px;
            border-radius: 2px;
            background: #0f52ba;
        }

        .search-wrapper.active .input-holder .search-icon span::before {
            background: #ffffff;
        }

        .search-wrapper .input-holder .search-icon span::after {
            width: 14px;
            height: 14px;
            left: 0px;
            top: 0px;
            border-radius: 16px;
            border: 4px solid #0f52ba;
        }

        .search-wrapper.active .input-holder .search-icon span::after {
            border: 4px solid #ffffff;
        }

        .search-wrapper .close {
            position: absolute;
            z-index: 1;
            top: 20px;
            right: 15px;
            width: 20px;
            height: 20px;
            cursor: pointer;
            transform: rotate(-180deg);
            opacity: 0;
            transition: all .3s cubic-bezier(0.285, -0.450, 0.935, 0.110);
            transition-delay: 0.2s;
            pointer-events: none;
        }

        .search-wrapper.active .close {
            right: 0px;
            transform: rotate(45deg);
            opacity: 1;
            pointer-events: auto;
            transition: all .6s cubic-bezier(0.000, 0.105, 0.035, 1.570);
            transition-delay: 0.3s;
        }

        .search-wrapper .close::before,
        .search-wrapper .close::after {
            position: absolute;
            content: '';
            background: #94a3b8;
            border-radius: 2px;
        }

        .search-wrapper .close::before {
            width: 4px;
            height: 20px;
            left: 8px;
            top: 0px;
        }

        .search-wrapper .close::after {
            width: 20px;
            height: 4px;
            left: 0px;
            top: 8px;
        }
        
        .search-wrapper .close:hover::before,
        .search-wrapper .close:hover::after {
            background: #dc2626;
        }
    </style>
</head>
<body>

  <div class="search-wrapper">
    <div class="input-holder">
      <input type="text" class="search-input" placeholder="Type to search..." />
      <button class="search-icon" onclick="searchToggle(this, event);"><span></span></button>
    </div>
    <span class="close" onclick="searchToggle(this, event);"></span>
  </div>

  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>
  <script>
    function searchToggle(obj, evt) {
        var container = $(obj).closest('.search-wrapper');
        if (!container.hasClass('active')) {
            container.addClass('active');
            evt.preventDefault();
            // Focus the input when opened
            setTimeout(function() {
                container.find('.search-input').focus();
            }, 500);
        }
        else if (container.hasClass('active') && $(obj).closest('.input-holder').length == 0) {
            container.removeClass('active');
            // clear input
            container.find('.search-input').val('');
        }
    }
  </script>

</body>
</html>
"""
