{
  description = "Flake for the Hermes retail product.";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flakelight.url = "github:nix-community/flakelight";
    poetry2nixl = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, flakelight, nixpkgs, poetry2nix, ... }:

    flakelight ./. {
      inputs.nixpkgs = nixpkgs;
      nixpkgs.config = { allowUnfree = true; };

      withOverlays = [ poetry2nix.overlays.default ];

      devShell = pkgs:
        let

          pypkgs-build-requirements = {
            pyright = [ "setuptools" ];
            stockfish = [ "setuptools" ];
          };
          # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md
          # EDGECASE WORKAROUND
          poetry2nix-overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend
            (final: prev:
              builtins.mapAttrs (package: build-requirements:
                (builtins.getAttr package prev).overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg:
                    if builtins.isString pkg then
                      builtins.getAttr pkg prev
                    else
                      pkg) build-requirements);
                })) pypkgs-build-requirements);

          poetryPkgs = pkgs.poetry2nix.mkPoetryEnv {
            projectDir = self;
            python = pkgs.python312;

            overrides = poetry2nix-overrides;
          };
        in pkgs.mkShell {

          packages = let
            basePkgs = with pkgs; [
              lefthook
              ngrok
              poetry

              coreutils

              commitlint-rs

              bruno
              nodejs
            ];
          in [ poetryPkgs ] ++ basePkgs;

        };
    };

}
