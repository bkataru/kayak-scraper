{ pkgs }: {
  deps = [
    pkgs.gh
	pkgs.geckodriver
	pkgs.ungoogled-chromium
	pkgs.chromedriver
  ];
}