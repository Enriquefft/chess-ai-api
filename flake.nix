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

      withOverlays = [
        poetry2nix.overlays.default

      ];

      devShell = pkgs:
        let

          poetryPkgs = pkgs.poetry2nix.mkPoetryEnv {
            projectDir = self;
            python = pkgs.python312;

            overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend

              (final: prev: {
                stockfish = prev.stockfish.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
                });
              });
          };

        in pkgs.mkShell {

          packages = [
            poetryPkgs
            pkgs.poetry

          ];
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

        };
    };

}
