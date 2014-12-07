package app.controllers;

import goja.mvc.Controller;
import com.jfinal.core.ActionKey;

/**
 * <p>
 * Default index Controller.
 * </p>
 */
public class IndexController extends Controller {

    @ActionKey("/")
    public void index(){
    	setAttr("app_name", "{{appName}}");
        render("/index.ftl");
    }
}